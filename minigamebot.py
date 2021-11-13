# インストールした discord.py を読み込む
import discord
import random

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'ODQ0NTk1NjY5ODk3NTc2NDg4.YKUtAw.VWT7dO5HncBfTZOieuCQIRTLplY'

# サーバのメインチャンネル設定によって置き換える
MAINCHANNEL_ID = 844596635740405823 # 任意のチャンネルID(int)

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('起動完了')
    # 起動したらbot名を発言
    mainchannel = client.get_channel(MAINCHANNEL_ID)
    await mainchannel.send('ミニゲームbotとして起動(できること：じゃんけん)')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # じゃんけんを開始する処理
    if message.content == 'じゃんけん':
        await janken_start(message.channel)
    # DMを送る処理
    if message.content == 'DM送って':
        await DM_send(message)

# リアクション受信時に動作する処理
@client.event
async def on_raw_reaction_add(payload):
        # リアクション送信者がBotだった場合は無視する
        if payload.member.bot:
            print('bot')
            return
        if payload.emoji.name == '✊' or payload.emoji.name == '✌️' or payload.emoji.name == '✋':
            print('get')
            await janken_play(payload)


# じゃんけん関数
async def janken_start(channel):
    await channel.send('最初はグー✊')
    game_massage = await channel.send('じゃんけんぽん！')
    await game_massage.add_reaction('✊')
    await game_massage.add_reaction('✌️')
    await game_massage.add_reaction('✋')

async def janken_play(payload):
    channel = client.get_channel(payload.channel_id)
    cpu_hand = random.randint(0,2)
    hand_emoji = ['✊', '✌️', '✋']
    if payload.emoji.name == '✊':
        player_hand = 0
        # print(payload.emoji)
        # print(payload.emoji.id)
        # await channel.send(payload.emoji.name)
    elif payload.emoji.name == '✌️':
        player_hand = 1
    elif payload.emoji.name == '✋':
        player_hand = 2

    player_name = payload.member.name

    if (player_hand+1)%3 == cpu_hand:
        await channel.send(player_name+':' + payload.emoji.name + '  bot:' + hand_emoji[cpu_hand])
        await channel.send('あなたの勝ちです')
    elif player_hand == (cpu_hand+1)%3:
        await channel.send(player_name+':' + payload.emoji.name + '  bot:' + hand_emoji[cpu_hand])
        await channel.send('あなたの負けです')
    elif player_hand == cpu_hand:
        await channel.send(player_name+':' + payload.emoji.name + '  bot:' + hand_emoji[cpu_hand])
        game_massage = await channel.send('あいこでしょ！')
        await game_massage.add_reaction('✊')
        await game_massage.add_reaction('✌️')
        await game_massage.add_reaction('✋')

# DM送る関数
async def DM_send(message):
    DM_channel = await message.author.create_dm()
    await DM_channel.send('やっほー')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

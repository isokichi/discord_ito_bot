# インストールした discord.py を読み込む
import discord
import random

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'OTA5MDI3NjY2NDE2NTMzNTY0.YY-T_A.vpVJzEPjNHij8F3XpjbuojJe_mo'

# サーバのメインチャンネル設定によって置き換える
# MAINCHANNEL_ID = 844596635740405823 # 任意のチャンネルID(int)
MAINCHANNEL_ID = 802372810013409292 # 任意のチャンネルID(int)

# 接続に必要なオブジェクトを生成
client = discord.Client()

player_list = []
ito_nums = []
ito_game_flag = False


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('起動完了')
    # 起動したらbot名を発言
    mainchannel = client.get_channel(MAINCHANNEL_ID)
    await mainchannel.send('ito bot 起動完了')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.content == 'ito':
        await ito_setting(message.channel)
    if message.content == '開始':
        await ito_start(message.channel)
    # じゃんけんを開始する処理
    if message.content == 'じゃんけん':
        await janken_start(message.channel)
    # DMを送る処理
    if message.content == 'DM送って':
        await DM_send(message)


# リアクション受信時に動作する処理
@client.event
async def on_raw_reaction_add(payload):
    global player_list, ito_nums, ito_game_flag
    # リアクション送信者がBotだった場合は無視する
    if payload.member.bot:
        # print('bot')
        return
    if payload.emoji.name == '✊' or payload.emoji.name == '✌️' or payload.emoji.name == '✋':
        print('get')
        await janken_play(payload)
    if payload.emoji.name == '✅':
        for itoplayer in player_list:
            if itoplayer == payload.member:
                return
        player_list.append(payload.member)
        print('new player:'+payload.member.name)
    if payload.emoji.name == '1️⃣' and ito_game_flag == True:
        await ito_send_dm(1)
    if payload.emoji.name == '2️⃣' and ito_game_flag == True:
        await ito_send_dm(2)
    if payload.emoji.name == '3️⃣' and ito_game_flag == True:
        await ito_send_dm(3)



async def ito_setting(channel):
    global player_list, ito_nums, ito_game_flag
    player_list = []
    await channel.send('itoをはじめます')
    await channel.send('参加者は✅を押してください')
    start_massage = await channel.send('準備ができたら「開始」と言ってください')
    await start_massage.add_reaction('✅')

async def ito_start(channel):
    global player_list, ito_nums, ito_game_flag
    ito_game_flag = True
    for i in range(0, 101):
        ito_nums.append(i)
    start_massage = await channel.send('何ターン目を開始しますか？')
    await start_massage.add_reaction('1️⃣')
    await start_massage.add_reaction('2️⃣')
    await start_massage.add_reaction('3️⃣')

async def ito_send_dm(ito_tern):
    global player_list, ito_nums, ito_game_flag
    for player in player_list:
        for i in range(0, ito_tern):
            target_num = random.randint(0,len(ito_nums))
            DM_channel = await player.create_dm()
            await DM_channel.send(target_num)
            ito_nums.pop(target_num)

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

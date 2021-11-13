# https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f

# インストールした discord.py を読み込む
import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'ODQ0NTk1NjY5ODk3NTc2NDg4.YKUtAw.VWT7dO5HncBfTZOieuCQIRTLplY'

# サーバのメインチャンネル設定によって置き換える
CHANNEL_ID = 844596635740405823 # 任意のチャンネルID(int)

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('起動完了')
    # 起動したらbot名を発言
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('猫botとして起動')



# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

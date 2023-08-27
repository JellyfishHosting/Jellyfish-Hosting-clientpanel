from urllib import parse
secret_key = "e77uE7IKVtg2WF@5FZ59MIkUIgE1yv9Q%Kl"
token = "MTE0MTg1ODAyNzgzODkwNjQwOA.GrWskV._CIwK-pBgeJfqSta3DI-GlACcRqcl23XHGTDzs"
client_secret = "9F6rxP159vhePN9m7IEl5Emz_wuLhgiU"
client_id = "1141858027838906408"
redirect_uri = "http://localhost:5000/oauth/discord/callback"
oauth_uri = f"https://discord.com/api/oauth2/authorize?client_id=1141858027838906408&redirect_uri={parse.quote(redirect_uri)}&response_type=code&scope=guilds%20guilds.join%20identify%20email"
mongo_db_password = "J8zeUKCeGGNinWRl"
mongo_uri = f"mongodb+srv://robinlongll77:{mongo_db_password}@cluster0.btj4thg.mongodb.net/?retryWrites=true&w=majority"
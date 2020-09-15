import sqlite3
from sqlite3 import Error
import discord

token = open("token.txt", "r").read()
client = discord.Client()

# ? Database

database_file = r"database.db"

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

conn = create_connection(database_file)

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    sql_create_students_table = """CREATE TABLE IF NOT EXISTS students (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    GPA integer NOT NULL,
                                    major text NOT NULL
                                );"""

    # create tables
    if conn is not None:
        create_table(conn, sql_create_students_table)
    else:
        print("Error! cannot create the database connection.")
main()


def execute_query(query):
    if conn is not None:
        try:            
            output = ""
            c = conn.cursor()
            try:
                c.execute(query)
            except Exception as e:
                return e
            info = c.fetchall()
            conn.commit()
            for value in info:
                output += str(value) + "\n"
            return output
        except Exception as e:
            return e
    return "Error! the database connection was not created."
        


# ? Discord Bot


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    client.CustomActivity(database_file, *, emoji=None)

title = 'SQLite Discord Shell'
arg_missing_message = discord.Embed(title=title, description='Arguments are missing')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    

    if message.content == ('>_help'):
        await message.channel.send(embed=(discord.Embed(title=title, description="""For More Help, visit SQLite's website:
         https://www.sqlite.org/doclist.html
         """, color=discord.Color.blue())))
        return


    if message.content.startswith('>_'):
        query = ""
        for word in message.content.split():
            query += word + " "
        query = query.replace('>_', '')
        if(query == " "):
            await message.channel.send(embed=arg_missing_message)
            return
        await message.channel.send(embed=discord.Embed(title=title + " Query Input:", description=(""" Query Sent: """ + query), color=discord.Color.red()))
        await message.channel.send(embed=(discord.Embed(title=title + " Query Output:", description=str(execute_query(query)), color=discord.Color.green())))
        # await message.channel.send(embed=arg_missing_message)

client.run(token)
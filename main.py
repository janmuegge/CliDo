import typer
import sqlite3

con = sqlite3.connect("todo.db")
cur = con.cursor()
app = typer.Typer()

def db_handler(todo, ifdone, action):
    
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (todo TEXT, ifdone BOOLEAN)")
    
    if action == "add":
        cur.execute("INSERT INTO tasks (todo, ifdone) VALUES (?, ?)", (todo, ifdone))
        con.commit()
        con.close()
    elif action == "remove":
        cur.execute("DELETE FROM tasks WHERE todo = ?", (todo,))
        con.commit()
        con.close()
    elif action == "list":
        cur.execute("SELECT * FROM tasks")
        for row in cur:
            row_check = ["Ja" if row[1] else "Nein"]
            print("Todo: ", row[0], " | Erledigt: ", row_check)
        count = cur.execute("SELECT COUNT(*) FROM tasks;")
        print()
        print(count.fetchone()[0], "Todos in der Datenbank")
        con.close()
    elif action == "complete":
        cur.execute("UPDATE tasks SET ifdone = ? WHERE todo = ?", (ifdone, todo))
        con.commit()
        con.close()

# Add Todo
@app.command()
def add(todo: str = typer.Argument(help="Todos hinzufügen..")):
    if todo.strip() == "":
        print("Es wurde kein Todo hinzugefügt, bitte einen variabeln angeben")
    else:
        print("Es wurde ein Todo hinzugefügt")
        db_handler(todo, ifdone=False, action="add")

# Remove Todo
@app.command()
def remove(todo: str = typer.Argument(help="Todos entfernen")):
    if todo.strip() == "":
        print("Es wurde keine Todo gefunden")
    else:
        db_handler(todo, None, action="remove")
        print("Es wurde ein Todo entfernt")
        
# Edit Todo
@app.command()
def edit(todo: str = typer.Argument(help="Todos bearbeiten")):
    if todo.strip() == "":
        print("Es wurde kein Todo bearbeitet")
    else:
        print("Es wurde ein Todo bearbeitet")

# Complete Todo
@app.command()
def complete(todo: str = typer.Argument(help="Todos abschließen")):
    if todo.strip() == "":
        print("Es wurde kein Todo abgeschlossen")
    else:
        db_handler(todo, True, action="complete")
        print("Es wurde ein Todo abgeschlossen")

# List Todos
@app.command()
def list_todo():
    db_handler(None, None, action="list")  

if __name__ == "__main__":
    app()
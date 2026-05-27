import json
import os

FILE_NAME = "todo_list.json"

# Load tasks
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

# Save tasks
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# Show tasks
def show_tasks(tasks):
    if not tasks:
        print("📭 Tidak ada tugas.")
        return
    print("\n📋 Daftar Tugas:")
    for i, task in enumerate(tasks):
        status = "✅" if task["done"] else "❌"
        print(f"{i + 1}. {task['title']} [{status}]")

# Add task
def add_task(tasks):
    title = input("Masukkan tugas: ")
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("✅ Tugas ditambahkan!")

# Mark done
def mark_done(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Pilih nomor tugas: ")) - 1
        tasks[index]["done"] = True
        save_tasks(tasks)
        print("🎉 Tugas selesai!")
    except:
        print("⚠️ Input tidak valid!")

# Delete task
def delete_task(tasks):
    show_tasks(tasks)
    try:
        index = int(input("Pilih nomor tugas: ")) - 1
        tasks.pop(index)
        save_tasks(tasks)
        print("🗑️ Tugas dihapus!")
    except:
        print("⚠️ Input tidak valid!")

# Main program
def main():
    tasks = load_tasks()

    while True:
        print("\n=== TO-DO LIST ===")
        print("1. Lihat tugas")
        print("2. Tambah tugas")
        print("3. Tandai selesai")
        print("4. Hapus tugas")
        print("5. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("👋 Keluar...")
            break
        else:
            print("⚠️ Pilihan tidak valid!")

if __name__ == "__main__":
    main()

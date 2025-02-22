from pathlib import Path
# Путь до папки клиента
folder = Path(r"C:\Users\Mikhail\Desktop\git\unik\sadm\lab1")

# Путь до изображения графа в папке клиента
graph_img_path = Path(folder, "graph_img.png")

chart_folder = Path(Path.cwd(), "img")

chart_filename = "gantt_chart.png"
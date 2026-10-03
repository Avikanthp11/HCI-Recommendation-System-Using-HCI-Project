import tkinter as tk
from tkinter import ttk, messagebox
from recommender import MovieRecommender

class RecommendationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SmartMovie AI - Recommendation System")
        self.geometry("920x650")
        self.minsize(800, 560)
        self.engine = MovieRecommender()
        self.movie = tk.StringVar(value="Orbit Rescue")
        self.genre = tk.StringVar(value="All Genres")
        self.count = tk.IntVar(value=5)
        self.build_ui()

    def build_ui(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Arial", 22, "bold"))
        style.configure("Action.TButton", font=("Arial", 11, "bold"), padding=10)

        outer = ttk.Frame(self, padding=24)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="SmartMovie AI", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Content-based recommendations using TF-IDF and cosine similarity."
        ).pack(anchor="w", pady=(2, 18))

        panel = ttk.LabelFrame(outer, text="Preferences", padding=15)
        panel.pack(fill="x")
        ttk.Label(panel, text="Choose a movie:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Combobox(
            panel, textvariable=self.movie, values=self.engine.titles(),
            state="readonly", width=40
        ).grid(row=0, column=1, sticky="ew", padx=10, pady=6)

        ttk.Label(panel, text="Genre filter:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(
            panel, textvariable=self.genre, values=self.engine.genres(),
            state="readonly", width=24
        ).grid(row=1, column=1, sticky="w", padx=10, pady=6)

        ttk.Label(panel, text="Results:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Spinbox(
            panel, from_=3, to=10, textvariable=self.count, width=7, state="readonly"
        ).grid(row=2, column=1, sticky="w", padx=10, pady=6)

        ttk.Button(
            panel, text="Get Recommendations", style="Action.TButton",
            command=self.show_results
        ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        panel.columnconfigure(1, weight=1)

        results = ttk.LabelFrame(outer, text="Recommended for you", padding=10)
        results.pack(fill="both", expand=True, pady=(18, 0))
        cols = ("rank", "title", "genres", "score", "why")
        self.tree = ttk.Treeview(results, columns=cols, show="headings", height=12)
        for key, label in zip(cols, ["#", "Movie", "Genres", "Similarity", "Why recommended"]):
            self.tree.heading(key, text=label)
        self.tree.column("rank", width=40, anchor="center", stretch=False)
        self.tree.column("title", width=170)
        self.tree.column("genres", width=190)
        self.tree.column("score", width=85, anchor="center")
        self.tree.column("why", width=300)
        self.tree.pack(fill="both", expand=True)
        self.status = ttk.Label(outer, text="Choose a movie, then request recommendations.")
        self.status.pack(anchor="w", pady=(10, 0))

    def show_results(self):
        try:
            items = self.engine.recommend(
                self.movie.get(), self.count.get(), self.genre.get()
            )
        except Exception as exc:
            messagebox.showerror("Recommendation error", str(exc))
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, item in enumerate(items, 1):
            self.tree.insert("", "end", values=(
                i, item["title"], item["genres"],
                f'{item["score"]}%', item["explanation"]
            ))
        self.status.config(
            text=f'Showing {len(items)} recommendations based on "{self.movie.get()}".'
        )

if __name__ == "__main__":
    RecommendationApp().mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os
import geopandas as gpd

class GeographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geografia - Rozpoznaj Kraj")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")

        # Zmienne aplikacji
        self.score = 0
        self.attempts = 0
        self.current_country = None
        self.current_difficulty = "world"

        # Utworzenie interfejsu
        self.create_widgets()

        # Ładowanie danych geograficznych
        self.load_geography_data()

        # Rozpoczęcie pierwszej rundy
        self.start_new_round()

    def load_geography_data(self):
        try:
            # Ścieżka do pliku shapefile - dostosuj ją do swojej struktury katalogów
            shapefile_path = "data/ne_110m_admin_0_countries.shp"

            # Alternatywne ścieżki, jeśli plik nie znajduje się w katalogu data
            alternative_paths = [
                "ne_110m_admin_0_countries.shp",  # w katalogu głównym
                "../data/ne_110m_admin_0_countries.shp",  # jeden poziom wyżej
                os.path.join(os.path.expanduser("~"), "Downloads", "ne_110m_admin_0_countries.shp")  # w katalogu Downloads
            ]

            # Sprawdź, czy główna ścieżka istnieje
            if os.path.exists(shapefile_path):
                self.world_data = gpd.read_file(shapefile_path)
            else:
                # Spróbuj alternatywnych ścieżek
                for path in alternative_paths:
                    if os.path.exists(path):
                        shapefile_path = path
                        self.world_data = gpd.read_file(path)
                        break
                else:
                    # Jeśli nie znaleziono pliku, wyświetl instrukcje
                    messagebox.showinfo("Brak danych geograficznych",
                                        "Nie znaleziono pliku z danymi geograficznymi.\n\n"
                                        "Aby pobrać dane:\n"
                                        "1. Odwiedź stronę https://www.naturalearthdata.com/downloads/110m-cultural-vectors/\n"
                                        "2. Pobierz plik 'Admin 0 – Countries'\n"
                                        "3. Rozpakuj archiwum do katalogu 'data' w folderze aplikacji\n")

                    # Utwórz pusty GeoDataFrame
                    self.world_data = self.create_empty_geodataframe()
                    return

            # Sprawdź nazwy kolumn w danych
            if 'NAME' in self.world_data.columns:
                self.world_data = self.world_data.rename(columns={'NAME': 'name'})
            elif 'ADMIN' in self.world_data.columns:
                self.world_data = self.world_data.rename(columns={'ADMIN': 'name'})

            # Sprawdź, czy jest kolumna z kontynentami
            if 'CONTINENT' in self.world_data.columns:
                self.world_data = self.world_data.rename(columns={'CONTINENT': 'continent'})
            elif 'REGION_WB' in self.world_data.columns:
                self.world_data = self.world_data.rename(columns={'REGION_WB': 'continent'})
            elif 'REGION_UN' in self.world_data.columns:
                self.world_data = self.world_data.rename(columns={'REGION_UN': 'continent'})
            else:
                # Jeśli nie ma kolumny z kontynentami, użyj przybliżonych wartości
                self.world_data['continent'] = "Unknown"

                # Przypisanie kontynentów na podstawie położenia (bardzo uproszczone)
                europe_countries = ['Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina',
                                    'Bulgaria', 'Croatia', 'Czech Republic', 'Denmark', 'Estonia', 'Finland',
                                    'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy',
                                    'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova',
                                    'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland',
                                    'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia',
                                    'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City']

                asia_countries = ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan',
                                  'Brunei', 'Cambodia', 'China', 'Cyprus', 'Georgia', 'India', 'Indonesia',
                                  'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan',
                                  'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal',
                                  'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar',
                                  'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan',
                                  'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey', 'Turkmenistan', 'United Arab Emirates',
                                  'Uzbekistan', 'Vietnam', 'Yemen']

                africa_countries = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi',
                                    'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros',
                                    'Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini',
                                    'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast',
                                    'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali',
                                    'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger',
                                    'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles',
                                    'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania',
                                    'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']

                north_america_countries = ['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada',
                                           'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador',
                                           'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico',
                                           'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia',
                                           'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States']

                south_america_countries = ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador',
                                           'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']

                oceania_countries = ['Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia',
                                     'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands',
                                     'Tonga', 'Tuvalu', 'Vanuatu']

                # Przypisanie kontynentów na podstawie nazw krajów
                for i, row in self.world_data.iterrows():
                    country_name = row['name']
                    if country_name in europe_countries:
                        self.world_data.at[i, 'continent'] = 'Europe'
                    elif country_name in asia_countries:
                        self.world_data.at[i, 'continent'] = 'Asia'
                    elif country_name in africa_countries:
                        self.world_data.at[i, 'continent'] = 'Africa'
                    elif country_name in north_america_countries:
                        self.world_data.at[i, 'continent'] = 'North America'
                    elif country_name in south_america_countries:
                        self.world_data.at[i, 'continent'] = 'South America'
                    elif country_name in oceania_countries:
                        self.world_data.at[i, 'continent'] = 'Oceania'

            # Słownik z polskimi nazwami krajów
            polish_names = {
                'Afghanistan': ['afganistan'],
                'Albania': ['albania'],
                'Algeria': ['algieria'],
                'Andorra': ['andora'],
                'Angola': ['angola'],
                'Antigua and Barbuda': ['antigua i barbuda'],
                'Argentina': ['argentyna'],
                'Armenia': ['armenia'],
                'Australia': ['australia'],
                'Austria': ['austria'],
                'Azerbaijan': ['azerbejdżan'],
                'Bahamas': ['bahamy'],
                'Bahrain': ['bahrajn'],
                'Bangladesh': ['bangladesz'],
                'Barbados': ['barbados'],
                'Belarus': ['białoruś'],
                'Belgium': ['belgia'],
                'Belize': ['belize'],
                'Benin': ['benin'],
                'Bhutan': ['bhutan'],
                'Bolivia': ['boliwia'],
                'Bosnia and Herzegovina': ['bośnia i hercegowina'],
                'Botswana': ['botswana'],
                'Brazil': ['brazylia'],
                'Brunei': ['brunei'],
                'Bulgaria': ['bułgaria'],
                'Burkina Faso': ['burkina faso'],
                'Burundi': ['burundi'],
                'Cambodia': ['kambodża'],
                'Cameroon': ['kamerun'],
                'Canada': ['kanada'],
                'Cape Verde': ['republika zielonego przylądka', 'zielony przylądek'],
                'Central African Republic': ['republika środkowoafrykańska'],
                'Chad': ['czad'],
                'Chile': ['chile'],
                'China': ['chiny'],
                'Colombia': ['kolumbia'],
                'Comoros': ['komory'],
                'Costa Rica': ['kostaryka'],
                'Croatia': ['chorwacja'],
                'Cuba': ['kuba'],
                'Cyprus': ['cypr'],
                'Czech Republic': ['czechy', 'republika czeska'],
                'Democratic Republic of the Congo': ['demokratyczna republika konga'],
                'Denmark': ['dania'],
                'Djibouti': ['dżibuti'],
                'Dominica': ['dominika'],
                'Dominican Republic': ['dominikana', 'republika dominikańska'],
                'East Timor': ['timor wschodni'],
                'Ecuador': ['ekwador'],
                'Egypt': ['egipt'],
                'El Salvador': ['salwador'],
                'Equatorial Guinea': ['gwinea równikowa'],
                'Eritrea': ['erytrea'],
                'Estonia': ['estonia'],
                'Eswatini': ['eswatini', 'suazi'],
                'Ethiopia': ['etiopia'],
                'Fiji': ['fidżi'],
                'Finland': ['finlandia'],
                'France': ['francja'],
                'Gabon': ['gabon'],
                'Gambia': ['gambia'],
                'Georgia': ['gruzja'],
                'Germany': ['niemcy'],
                'Ghana': ['ghana'],
                'Greece': ['grecja'],
                'Grenada': ['grenada'],
                'Guatemala': ['gwatemala'],
                'Guinea': ['gwinea'],
                'Guinea-Bissau': ['gwinea bissau'],
                'Guyana': ['gujana'],
                'Haiti': ['haiti'],
                'Honduras': ['honduras'],
                'Hungary': ['węgry'],
                'Iceland': ['islandia'],
                'India': ['indie'],
                'Indonesia': ['indonezja'],
                'Iran': ['iran'],
                'Iraq': ['irak'],
                'Ireland': ['irlandia'],
                'Israel': ['izrael'],
                'Italy': ['włochy'],
                'Ivory Coast': ['wybrzeże kości słoniowej'],
                'Jamaica': ['jamajka'],
                'Japan': ['japonia'],
                'Jordan': ['jordania'],
                'Kazakhstan': ['kazachstan'],
                'Kenya': ['kenia'],
                'Kiribati': ['kiribati'],
                'Kosovo': ['kosowo'],
                'Kuwait': ['kuwejt'],
                'Kyrgyzstan': ['kirgistan'],
                'Laos': ['laos'],
                'Latvia': ['łotwa'],
                'Lebanon': ['liban'],
                'Lesotho': ['lesotho'],
                'Liberia': ['liberia'],
                'Libya': ['libia'],
                'Liechtenstein': ['liechtenstein'],
                'Lithuania': ['litwa'],
                'Luxembourg': ['luksemburg'],
                'Madagascar': ['madagaskar'],
                'Malawi': ['malawi'],
                'Malaysia': ['malezja'],
                'Maldives': ['malediwy'],
                'Mali': ['mali'],
                'Malta': ['malta'],
                'Marshall Islands': ['wyspy marshalla'],
                'Mauritania': ['mauretania'],
                'Mauritius': ['mauritius'],
                'Mexico': ['meksyk'],
                'Micronesia': ['mikronezja'],
                'Moldova': ['mołdawia'],
                'Monaco': ['monako'],
                'Mongolia': ['mongolia'],
                'Montenegro': ['czarnogóra'],
                'Morocco': ['maroko'],
                'Mozambique': ['mozambik'],
                'Myanmar': ['birma', 'mjanma'],
                'Namibia': ['namibia'],
                'Nauru': ['nauru'],
                'Nepal': ['nepal'],
                'Netherlands': ['holandia', 'niderlandy'],
                'New Zealand': ['nowa zelandia'],
                'Nicaragua': ['nikaragua'],
                'Niger': ['niger'],
                'Nigeria': ['nigeria'],
                'North Korea': ['korea północna'],
                'North Macedonia': ['macedonia północna'],
                'Norway': ['norwegia'],
                'Oman': ['oman'],
                'Pakistan': ['pakistan'],
                'Palau': ['palau'],
                'Palestine': ['palestyna'],
                'Panama': ['panama'],
                'Papua New Guinea': ['papua-nowa gwinea'],
                'Paraguay': ['paragwaj'],
                'Peru': ['peru'],
                'Philippines': ['filipiny'],
                'Poland': ['polska'],
                'Portugal': ['portugalia'],
                'Qatar': ['katar'],
                'Republic of the Congo': ['republika konga', 'kongo'],
                'Romania': ['rumunia'],
                'Russia': ['rosja'],
                'Rwanda': ['rwanda'],
                'Saint Kitts and Nevis': ['saint kitts i nevis'],
                'Saint Lucia': ['saint lucia'],
                'Saint Vincent and the Grenadines': ['saint vincent i grenadyny'],
                'Samoa': ['samoa'],
                'San Marino': ['san marino'],
                'Saudi Arabia': ['arabia saudyjska'],
                'Senegal': ['senegal'],
                'Serbia': ['serbia'],
                'Seychelles': ['seszele'],
                'Sierra Leone': ['sierra leone'],
                'Singapore': ['singapur'],
                'Slovakia': ['słowacja'],
                'Slovenia': ['słowenia'],
                'Solomon Islands': ['wyspy salomona'],
                'Somalia': ['somalia'],
                'South Africa': ['republika południowej afryki', 'rpa'],
                'South Korea': ['korea południowa'],
                'South Sudan': ['sudan południowy'],
                'Spain': ['hiszpania'],
                'Sri Lanka': ['sri lanka'],
                'Sudan': ['sudan'],
                'Suriname': ['surinam'],
                'Sweden': ['szwecja'],
                'Switzerland': ['szwajcaria'],
                'Syria': ['syria'],
                'Taiwan': ['tajwan'],
                'Tajikistan': ['tadżykistan'],
                'Tanzania': ['tanzania'],
                'Thailand': ['tajlandia'],
                'Togo': ['togo'],
                'Tonga': ['tonga'],
                'Trinidad and Tobago': ['trynidad i tobago'],
                'Tunisia': ['tunezja'],
                'Turkey': ['turcja'],
                'Turkmenistan': ['turkmenistan'],
                'Tuvalu': ['tuvalu'],
                'Uganda': ['uganda'],
                'Ukraine': ['ukraina'],
                'United Arab Emirates': ['zjednoczone emiraty arabskie', 'emiraty arabskie', 'zea'],
                'United Kingdom': ['wielka brytania', 'zjednoczone królestwo', 'anglia', 'uk'],
                'United States': ['stany zjednoczone', 'usa', 'ameryka'],
                'Uruguay': ['urugwaj'],
                'Uzbekistan': ['uzbekistan'],
                'Vanuatu': ['vanuatu'],
                'Vatican City': ['watykan'],
                'Venezuela': ['wenezuela'],
                'Vietnam': ['wietnam'],
                'Yemen': ['jemen'],
                'Zambia': ['zambia'],
                'Zimbabwe': ['zimbabwe']
            }

            # Dodanie kolumny z alternatywnymi nazwami
            self.world_data['alt_names'] = self.world_data['name'].apply(
                lambda x: polish_names.get(x, []) + [x.lower()]
            )

            print(f"Załadowano {len(self.world_data)} krajów")

            # Zapisanie granic całego świata do późniejszego użycia
            self.world_bounds = self.world_data.total_bounds

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się załadować danych geograficznych: {str(e)}")
            self.world_data = self.create_empty_geodataframe()

    def create_empty_geodataframe(self):
        return gpd.GeoDataFrame(columns=['name', 'continent', 'alt_names', 'geometry'])

    def create_widgets(self):
        # Górny panel z tytułem i punktacją
        header_frame = tk.Frame(self.root, bg="#f5f5f5")
        header_frame.pack(fill=tk.X, padx=20, pady=10)

        title_label = tk.Label(header_frame, text="Geografia - Rozpoznaj Kraj",
                               font=("Segoe UI", 18, "bold"), bg="#f5f5f5")
        title_label.pack(side=tk.LEFT)

        stats_frame = tk.Frame(header_frame, bg="#f5f5f5")
        stats_frame.pack(side=tk.RIGHT)

        tk.Label(stats_frame, text="Punkty:", bg="#f5f5f5", font=("Segoe UI", 12)).pack(side=tk.LEFT)
        self.score_label = tk.Label(stats_frame, text="0", bg="#f5f5f5", font=("Segoe UI", 12, "bold"))
        self.score_label.pack(side=tk.LEFT, padx=(5, 15))

        tk.Label(stats_frame, text="Celność:", bg="#f5f5f5", font=("Segoe UI", 12)).pack(side=tk.LEFT)
        self.accuracy_label = tk.Label(stats_frame, text="0%", bg="#f5f5f5", font=("Segoe UI", 12, "bold"))
        self.accuracy_label.pack(side=tk.LEFT, padx=(5, 0))

        # Ramka dla mapy
        self.map_frame = tk.Frame(self.root, bg="white")
        self.map_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Utworzenie figury Matplotlib z określoną wielkością i DPI
        self.fig, self.ax = plt.subplots(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Panel odpowiedzi
        answer_frame = tk.Frame(self.root, bg="white", pady=15, padx=20)
        answer_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(answer_frame, text="Jaki to kraj?", bg="white", font=("Segoe UI", 12)).pack()

        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(answer_frame, textvariable=self.answer_var, font=("Segoe UI", 12), width=30)
        answer_entry.pack(pady=10)
        answer_entry.bind("<Return>", lambda e: self.check_answer())

        button_frame = tk.Frame(answer_frame, bg="white")
        button_frame.pack(pady=5)

        check_btn = ttk.Button(button_frame, text="Sprawdź", command=self.check_answer)
        check_btn.pack(side=tk.LEFT, padx=5)

        next_btn = ttk.Button(button_frame, text="Następny kraj", command=self.start_new_round)
        next_btn.pack(side=tk.LEFT, padx=5)

        self.feedback_label = tk.Label(answer_frame, text="", bg="white", font=("Segoe UI", 12, "bold"))
        self.feedback_label.pack(pady=10)

        # Panel wyboru trudności
        difficulty_frame = tk.Frame(self.root, bg="#f5f5f5")
        difficulty_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        tk.Label(difficulty_frame, text="Poziom trudności:", bg="#f5f5f5").pack(side=tk.LEFT)

        self.difficulty_var = tk.StringVar(value="world")
        difficulty_combo = ttk.Combobox(difficulty_frame, textvariable=self.difficulty_var, width=15)
        difficulty_combo['values'] = ('world', 'europe', 'asia', 'africa', 'americas', 'oceania')
        difficulty_combo.pack(side=tk.LEFT, padx=10)
        difficulty_combo.bind("<<ComboboxSelected>>", self.change_difficulty)

    def change_difficulty(self, event=None):
        self.current_difficulty = self.difficulty_var.get()
        self.start_new_round()

    def get_filtered_countries(self):
        if len(self.world_data) == 0:
            return gpd.GeoDataFrame()

        if self.current_difficulty == "world":
            return self.world_data
        elif self.current_difficulty == "europe":
            return self.world_data[self.world_data['continent'] == "Europe"]
        elif self.current_difficulty == "asia":
            return self.world_data[self.world_data['continent'] == "Asia"]
        elif self.current_difficulty == "africa":
            return self.world_data[self.world_data['continent'] == "Africa"]
        elif self.current_difficulty == "americas":
            return self.world_data[
                (self.world_data['continent'] == "North America") |
                (self.world_data['continent'] == "South America")
                ]
        elif self.current_difficulty == "oceania":
            return self.world_data[self.world_data['continent'] == "Oceania"]
        return self.world_data

    def start_new_round(self):
        # Wyczyszczenie pola odpowiedzi i informacji zwrotnej
        self.answer_var.set("")
        self.feedback_label.config(text="")

        # Filtrowanie krajów według poziomu trudności
        filtered_countries = self.get_filtered_countries()

        # Wybór losowego kraju
        if len(filtered_countries) > 0:
            random_index = random.randint(0, len(filtered_countries) - 1)
            self.current_country = filtered_countries.iloc[random_index]

            # Wyczyszczenie poprzedniego wykresu
            self.ax.clear()

            # Wyświetlenie mapy świata jako tło z lepszymi kolorami
            self.world_data.plot(ax=self.ax, color='#e0e0e0', edgecolor='#c0c0c0', linewidth=0.5)

            # Wyświetlenie wybranego kraju
            country_geom = filtered_countries[filtered_countries['name'] == self.current_country['name']]
            country_geom.plot(ax=self.ax, color='#66b3ff', edgecolor='#0066cc', linewidth=1)

            # Ukrycie etykiet osi
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_axis_off()

            # Przybliżenie do wybranego kraju z większym marginesem
            # Pobierz granice kraju
            minx, miny, maxx, maxy = country_geom.total_bounds

            # Oblicz środek kraju
            center_x = (minx + maxx) / 2
            center_y = (miny + maxy) / 2

            # Oblicz szerokość i wysokość kraju
            width = maxx - minx
            height = maxy - miny

            # Użyj większego z wymiarów do określenia skali
            size = max(width, height)

            # Dodaj znacznie większy margines (5x rozmiar kraju)
            margin_factor = 5.0  # Możesz dostosować tę wartość

            # Ustaw granice widoku mapy zachowując proporcje
            self.ax.set_xlim(center_x - size * margin_factor / 2, center_x + size * margin_factor / 2)
            self.ax.set_ylim(center_y - size * margin_factor / 2, center_y + size * margin_factor / 2)

            # Dodaj przycisk "Pokaż cały świat"
            show_world_btn = ttk.Button(self.map_frame, text="Pokaż cały świat",
                                        command=self.show_world_view)
            show_world_btn.place(relx=0.9, rely=0.05, anchor="ne")

            # Aktualizacja wykresu
            self.canvas.draw()
        else:
            messagebox.showwarning("Ostrzeżenie", "Brak krajów dla wybranego poziomu trudności")

    def show_world_view(self):
        """Przywraca widok całego świata"""
        if hasattr(self, 'world_bounds'):
            minx, miny, maxx, maxy = self.world_bounds
            self.ax.set_xlim(minx, maxx)
            self.ax.set_ylim(miny, maxy)
            self.canvas.draw()

    def check_answer(self):
        if not hasattr(self, 'current_country') or self.current_country is None:
            messagebox.showinfo("Informacja", "Najpierw rozpocznij nową rundę")
            return

        user_answer = self.answer_var.get().strip().lower()

        if not user_answer:
            messagebox.showinfo("Informacja", "Wpisz nazwę kraju")
            return

        correct_name = self.current_country['name']
        alt_names = self.current_country['alt_names']

        self.attempts += 1

        if user_answer in alt_names:
            self.score += 1
            self.feedback_label.config(text="Poprawna odpowiedź!", fg="#4CAF50")
        else:
            # Próbuj znaleźć polską nazwę kraju
            polish_name = ""
            for name in alt_names:
                if name not in [correct_name.lower()]:
                    polish_name = name
                    break

            if polish_name:
                self.feedback_label.config(text=f"Niestety, to jest {polish_name.capitalize()}", fg="#f44336")
            else:
                self.feedback_label.config(text=f"Niestety, to jest {correct_name}", fg="#f44336")

        # Aktualizacja punktacji
        self.score_label.config(text=str(self.score))
        accuracy = int((self.score / self.attempts) * 100) if self.attempts > 0 else 0
        self.accuracy_label.config(text=f"{accuracy}%")

# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = GeographyApp(root)
    root.mainloop()

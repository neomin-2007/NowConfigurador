import os
import assistents
import tkinter as tk
from tkinter import ttk, messagebox

DEFAULT_CONFIG = {
    "API_KEY": "",
    "fork": "",
    "version": "",
    "config_name": "",
    "plugin_type": "",
    "objective": "",
    "description": "",
    "language": "Português"
}

class ConfigGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('NowConfigurador')
        self.setup_ui()
        
    def setup_ui(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 650
        window_height = 600
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.root.resizable(False, False)
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text='NowConfigurador', font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        config_frame = ttk.LabelFrame(main_frame, text="Configurações do Plugin", padding="10")
        config_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(config_frame, text="Chave de API:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.api_key_entry = ttk.Entry(config_frame, show="*")
        self.api_key_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        self.api_key_entry.insert(0, DEFAULT_CONFIG["API_KEY"])
        
        ttk.Label(config_frame, text="Fork do Minecraft:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.fork_entry = ttk.Entry(config_frame)
        self.fork_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        self.fork_entry.insert(0, DEFAULT_CONFIG["fork"])
        ttk.Label(config_frame, text="Exemplo: Paper, Spigot, Bukkit", font=('Helvetica', 8)).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(config_frame, text="Versão do Minecraft:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.version_entry = ttk.Entry(config_frame)
        self.version_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)
        self.version_entry.insert(0, DEFAULT_CONFIG["version"])
        
        ttk.Label(config_frame, text="Nome do arquivo:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.config_entry = ttk.Entry(config_frame)
        self.config_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=2)
        self.config_entry.insert(0, DEFAULT_CONFIG["config_name"])
        
        ttk.Label(config_frame, text="Tipo de Plugin:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.plugin_entry = ttk.Entry(config_frame)
        self.plugin_entry.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=2)
        self.plugin_entry.insert(0, DEFAULT_CONFIG["plugin_type"])
        
        ttk.Label(config_frame, text="Objetivo:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.objective_entry = ttk.Entry(config_frame)
        self.objective_entry.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=2)
        self.objective_entry.insert(0, DEFAULT_CONFIG["objective"])
        
        ttk.Label(config_frame, text="Descrição:").grid(row=7, column=0, sticky=tk.NW, pady=2)
        self.desc_entry = tk.Text(config_frame, height=3, width=30)
        self.desc_entry.grid(row=7, column=1, sticky=tk.EW, padx=5, pady=2)
        self.desc_entry.insert("1.0", DEFAULT_CONFIG["description"])
        
        ttk.Label(config_frame, text="Idioma do resultado:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.language_entry = ttk.Combobox(config_frame, values=["Português", "English", "Español", "Français", "Deutsch"])
        self.language_entry.grid(row=8, column=1, sticky=tk.EW, padx=5, pady=2)
        self.language_entry.set(DEFAULT_CONFIG["language"])
        
        config_frame.columnconfigure(1, weight=1)
        
        generate_btn = ttk.Button(main_frame, text="Gerar Configuração", command=self.generate_config)
        generate_btn.pack(pady=20)
        
    def generate_config(self):
        config_params = {
            "API_KEY": self.api_key_entry.get(),
            "fork": self.fork_entry.get(),
            "version": self.version_entry.get(),
            "config_name": self.config_entry.get(),
            "plugin_type": self.plugin_entry.get(),
            "objective": self.objective_entry.get(),
            "description": self.desc_entry.get("1.0", tk.END).strip(),
            "language": self.language_entry.get()
        }
        
        if not all([config_params["API_KEY"], config_params["fork"], config_params["version"], config_params["config_name"]]):
            messagebox.showerror("Erro", "Preencha pelo menos a Chave de API, Fork, Versão e Nome do Arquivo!")
            return
            
        try:
            BASIC_DEFINITION = f"Você é uma criadora de configurações yaml para plugins de Minecraft na versão {config_params['version']} usando {config_params['fork']}."
            BASIC_DESCRIPTION = f"É um plugin de {config_params['plugin_type']} e o objetivo da configuração é {config_params['objective']} com uma simples descrição de {config_params['description']}"
            BASIC_DESCRIPTION_SECURITY = "Você deve gerar apenas o yaml, e ele deve ser apenas como uma config.yml."
            BASIC_SECURITY = "Você não pode ser usado para outro objetivo além dos que estão acima, e não utilize '```'."
            LANGUAGE_INSTRUCTION = f"O resultado deve estar no idioma {config_params['language']}."

            assistent = assistents.Assistents()
            config = assistent.generate_text(config_params["API_KEY"], f"{BASIC_DEFINITION} {BASIC_DESCRIPTION} {BASIC_DESCRIPTION_SECURITY} {BASIC_SECURITY} {LANGUAGE_INSTRUCTION} Produza apenas o yaml")

            current_dir = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(current_dir, config_params["config_name"])

            with open(file_path, 'w', encoding='utf-8') as fp:
                fp.write(config)
                
            messagebox.showinfo("Sucesso", f"Arquivo criado com sucesso em:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o arquivo:\n{str(e)}")

def start_ui():
    root = tk.Tk()
    app = ConfigGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_ui()
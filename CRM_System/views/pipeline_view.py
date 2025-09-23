import tkinter as tk
from tkinter import ttk

class PipelineView(ttk.Frame):
    def __init__(self, parent, opportunity_controller, i18n, user):
        super().__init__(parent)
        self.opportunity_controller = opportunity_controller
        self.i18n = i18n
        self.current_user = user
        self.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.draw_pipeline)

    def draw_pipeline(self, event=None):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        stages_data = self.opportunity_controller.get_opportunities_by_stage()
        
        # Define colors for each stage
        stage_colors = {
            "Prospección": "#ADD8E6",  # Light Blue
            "Cualificación": "#90EE90", # Light Green
            "Propuesta": "#FFD700",     # Gold
            "Negociación": "#FFA07A",  # Light Salmon
            "Ganado": "#32CD32",   # Lime Green
            "Perdido": "#FF6347"    # Tomato
        }

        # Ensure all stages from the database are included, even if not in hardcoded colors
        # This handles cases where new stages might be added or existing ones are different
        all_stages = list(stages_data.keys())
        # Sort stages to maintain a consistent order in the pipeline
        # For now, we'll use the order from the hardcoded list if available, otherwise alphabetical
        defined_order = ["Prospección", "Cualificación", "Propuesta", "Negociación", "Ganado", "Perdido"]
        sorted_stages = sorted(all_stages, key=lambda s: defined_order.index(s) if s in defined_order else len(defined_order) + all_stages.index(s))


        # Calculate total value for normalization
        total_value = sum(data["total_value"] for data in stages_data.values())
        
        if total_value == 0:
            self.canvas.create_text(canvas_width / 2, canvas_height / 2, text=self.i18n.get("main_window", "no_opportunities_in_pipeline"), font=("Arial", 12), fill="gray")
            return

        # Drawing parameters
        bar_height = 40
        padding = 10
        y_offset = padding
        
        # Calculate max value for dynamic bar width scaling
        max_value = max(data["total_value"] for data in stages_data.values()) if stages_data else 1

        for stage in sorted_stages:
            data = stages_data[stage]
            value = data["total_value"]
            count = data["count"]
            
            # Calculate bar width based on its proportion to the max value, not total value
            # This gives a better visual distinction between stages
            bar_width = (value / max_value) * (canvas_width - 2 * padding)
            if bar_width < 1: # Ensure even very small bars are visible
                bar_width = 1

            # Draw rectangle
            self.canvas.create_rectangle(
                padding, y_offset,
                padding + bar_width, y_offset + bar_height,
                fill=stage_colors.get(stage, "#CCCCCC"), # Default to light gray for undefined stages
                outline="black"
            )
            
            # Add text label
            text_label = f"{stage}: ${value:,.2f} ({count} {self.i18n.get('main_window', 'opportunities_label')})"
            self.canvas.create_text(
                padding + bar_width / 2, y_offset + bar_height / 2,
                text=text_label, font=("Arial", 10, "bold"), fill="black"
            )
            
            y_offset += bar_height + padding

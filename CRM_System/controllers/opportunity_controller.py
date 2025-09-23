from CRM_System.models.opportunity import Opportunity
from CRM_System.controllers.database_controller import DatabaseController

class OpportunityController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def create_opportunity(self, opportunity_data):
        query = """
            INSERT INTO opportunities (title, contact_id, value, stage, probability, close_date, description, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            opportunity_data.get('title', ''),
            opportunity_data.get('contact_id'),
            opportunity_data.get('value', 0.0),
            opportunity_data.get('stage', 'Prospección'),
            opportunity_data.get('probability', 10),
            opportunity_data.get('close_date'),
            opportunity_data.get('description', ''),
            opportunity_data.get('assigned_to')
        )
        self.db_controller.execute_query(query, params)

    def get_all_opportunities(self):
        query = "SELECT * FROM opportunities"
        results = self.db_controller.execute_query(query)
        opportunities = []
        for row in results:
            opportunity = Opportunity(row[1], row[2], row[3], row[4], row[5])
            opportunity.id = row[0]
            opportunities.append(opportunity)
        return opportunities

    def get_opportunity(self, opportunity_id):
        query = "SELECT * FROM opportunities WHERE id = ?"
        params = (opportunity_id,)
        results = self.db_controller.execute_query(query, params)
        if results:
            result = results[0]
            opportunity = Opportunity(result[1], result[2], result[3], result[4], result[5])
            opportunity.id = result[0]
            return opportunity
        return None

    def update_opportunity(self, opportunity_id, opportunity_data):
        query = """
            UPDATE opportunities
            SET title = ?, contact_id = ?, value = ?, stage = ?, probability = ?, close_date = ?, description = ?, assigned_to = ?
            WHERE id = ?
        """
        params = (
            opportunity_data.get('title', ''),
            opportunity_data.get('contact_id'),
            opportunity_data.get('value', 0.0),
            opportunity_data.get('stage', 'Prospección'),
            opportunity_data.get('probability', 10),
            opportunity_data.get('close_date'),
            opportunity_data.get('description', ''),
            opportunity_data.get('assigned_to'),
            opportunity_id
        )
        self.db_controller.execute_query(query, params)

    def delete_opportunity(self, opportunity_id):
        query = "DELETE FROM opportunities WHERE id = ?"
        params = (opportunity_id,)
        self.db_controller.execute_query(query, params)

    def clear_opportunities(self):
        query = "DELETE FROM opportunities"
        self.db_controller.execute_query(query)

    def get_opportunities_by_stage(self):
        stages_data = {}
        stages = ["Prospección", "Cualificación", "Propuesta", "Negociación", "Ganado", "Perdido"]
        for stage in stages:
            query = "SELECT COUNT(*), SUM(value) FROM opportunities WHERE stage = ?"
            params = (stage,)
            result = self.db_controller.execute_query(query, params)[0]
            count = result[0] if result[0] is not None else 0
            total_value = result[1] if result[1] is not None else 0.0
            stages_data[stage] = {"count": count, "total_value": total_value}
        return stages_data

    def calculate_forecast(self):
        total_forecast = 0
        opportunities = self.get_all_opportunities()
        for opp in opportunities:
            total_forecast += (opp.value * opp.probability) / 100
        return total_forecast

    def generate_stage_report(self):
        report = "Informe de Oportunidades por Etapa:\n\n"
        stages = {
            "Prospección": "Prospección",
            "Cualificación": "Cualificación",
            "Propuesta": "Propuesta",
            "Negociación": "Negociación",
            "Ganado": "Ganado",
            "Perdido": "Perdido"
        }
        
        for stage in stages:
            query = "SELECT COUNT(*) FROM opportunities WHERE stage = ?"
            params = (stage,)
            count = self.db_controller.execute_query(query, params)[0][0]
            report += f"{stages.get(stage, stage.capitalize())}: {count} oportunidades\n"
        
        return report

    def get_distinct_stages(self):
        query = "SELECT DISTINCT stage FROM opportunities"
        results = self.db_controller.execute_query(query)
        return [row[0] for row in results]

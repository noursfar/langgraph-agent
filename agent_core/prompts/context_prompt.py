# agent_core/prompts/context_prompt.py
import json
from agent_core.prompts.context_utils import get_pds, get_rooms, get_planned_entries
from agent_core.utils.exceptions import ContextBuildError
from agent_core.utils.logger import log


def build_context_prompt(pds_id = 269):
    """ Build a rich contextual prompt for the PDS assistant."""
    try:
        # Fetch PDS, rooms, and planned entries
        pds_json, sectors_names, _ = get_pds(pds_id)
        available_rooms, occupied_rooms = get_rooms()

        pds_info = json.loads(pds_json)
        hr_id = pds_info["healthcare_facility_id"]
        planned_entries = get_planned_entries(hr_id) if hr_id else []

        pds_summary = (
            f"Professionnel de santé (pds): {pds_info.get('pds_name')} ({pds_info.get('pds_gender')})\n"
            f"Spécialité : {pds_info.get('medical_staff_type')}\n"
            f"Département : {pds_info.get('department_name')}\n"
            f"Établissement : {pds_info.get('healthcare_facility_name')} "
            f"({pds_info.get('healthcare_facility_description')})"
        )

        sectors_summary = (
            f"Secteur(s) pris en charge par ce pds: {', '.join(sectors_names) if sectors_names else 'Non spécifiés'}"
        )

        rooms_summary = (
            f"Chambres disponibles : {available_rooms if available_rooms else 'Aucune chambre libre.'}\n"
            f"Chambres occupées : {occupied_rooms if occupied_rooms else 'Aucune chambre occupée.'}\n"
            "Chaque chambre est décrite sous la forme : "
            "[Numéro de chambre] : [Nom complet du patient] : [ID patient] : [Raison ou parcours médical du patient]."
        )

        if not planned_entries:
            planned_entries_summary = "Aucune entrée n’est prévue pour aujourd’hui."
        else:
            planned_entries_summary = (
                f"Entrées prévues pour aujourd’hui : {planned_entries}.\n"
                "Chaque entrée suit le format : "
                "[Nom et prénom du patient] : [Service médical] : [Date d’entrée prévue]."
            )

        # --- Combine all sections into one structured context ---
        context = (
            f"--- CONTEXTE DU PROFESSIONNEL DE SANTÉ ---\n{pds_summary}\n\n"
            f"--- SECTEURS D'INTERVENTION ---\n{sectors_summary}\n\n"
            f"--- DISPONIBILITÉ DES CHAMBRES ---\n{rooms_summary}\n\n"
            f"--- ENTRÉES PLANIFIÉES ---\n{planned_entries_summary}\n"
        )

        log.debug("Successfully built context prompt for PDS ID: %s", pds_id)
        return context

    except Exception as e:
        log.exception("Failed to build context prompt for PDS ID: %s", pds_id)
        raise ContextBuildError(f"Failed to build context prompt: {e}") from e

# agent_core/tools/get_patient_data.py
import asyncio, httpx
from langchain.tools import tool

from agent_core.tools import parse_and_validate_name_input
from agent_core.utils.logger import log
from agent_core.config.settings import settings
from agent_core.utils.exceptions import AgentToolError
from agent_core.utils.oauth import oauth_manager


@tool("get_patient_data", return_direct=False)
def get_patient_data(input_data):
    """
    Récupère les informations d’un patient spécifique à partir de son prénom et nom exacts.

    Args:
        input_data (str): dictionnaire contenant les clés "firstname" et "lastname".
    """
    firstname, lastname = parse_and_validate_name_input(input_data)
    log.info("Fetching PDS contact for: %s %s", firstname, lastname)

    try:
        token = asyncio.run(oauth_manager.get_access_token())
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{settings.springboot_healthcare_facility_url}/api/v1/patient?firstname={firstname}&lastname={lastname}"

        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        # Parse and format data
        results = []
        for entry in data:
            patient_dto = entry.get("patientDto", {})
            patient_id = patient_dto.get("id")

            # Pathway info
            pathway = entry.get("pathwayDto")
            pathway_name, treatments, effective_exit_date = None, [], None
            if pathway:
                pathway_type = pathway.get("pathwayType", {})
                pathway_name = pathway_type.get("name")
                effective_exit_date = pathway.get("effectiveExitDate")

                for pt_tt in pathway_type.get("pathwayTypeTreatmentType", []):
                    tt = pt_tt.get("treatmentType")
                    if tt and tt.get("name"):
                        treatments.append(tt["name"])

            # Room info
            room_summary = entry.get("roomSummaryDto")
            room_combined, sector_name = None, None
            if room_summary:
                room_number = room_summary.get("roomNumber")
                bed = room_summary.get("bed")
                sector_name = room_summary.get("sectorName")
                if room_number and bed:
                    room_combined = f"{room_number}{bed}"

            results.append({
                "patientId": patient_id,
                "pathwayName": pathway_name,
                "treatments": treatments,
                "effectiveExitDate": effective_exit_date,
                "room": room_combined,
                "sectorName": sector_name
            })

        log.info("Retrieved %d patient(s) matching %s %s", len(results), firstname, lastname)
        return results

    except Exception as e:
        log.exception("Unexpected error fetching patient data for %s %s", firstname, lastname)
        raise AgentToolError(f"Unexpected error: {e}") from e

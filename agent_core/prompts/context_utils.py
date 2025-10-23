# agent_core/prompts/context_utils.py
import json
import asyncio
import httpx
from agent_core.utils.logger import log
from agent_core.utils.oauth import oauth_manager
from agent_core.utils.exceptions import AgentToolError
from agent_core.config.settings import settings


def get_pds(pds_id):
    try:
        token = asyncio.run(oauth_manager.get_access_token())
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{settings.springboot_healthcare_facility_url}/api/v1/medical-staff/{pds_id}"

        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        account = data.get("account", {})
        pds_name = f"{account.get('firstname', '')} {account.get('lastname', '')}".strip()
        gender = account.get("gender", "Unknown")
        medical_staff_type = data.get("medicalStaffType", {}).get("name", "Unknown")
        department_name = data.get("department", {}).get("name", "Unknown")

        sectors = data.get("sectors", [])
        sectors_names = [s.get("name") for s in sectors if s.get("name")]
        sectors_ids = [s.get("id") for s in sectors if s.get("id")]

        healthcare_facility = data.get("healthcareFacilityDto", {})
        extracted_data = {
            "pds_name": pds_name,
            "pds_gender": gender,
            "medical_staff_type": medical_staff_type,
            "department_name": department_name,
            "healthcare_facility_id": healthcare_facility.get("id", ""),
            "healthcare_facility_name": healthcare_facility.get("name", ""),
            "healthcare_facility_description": healthcare_facility.get("description", "")
        }

        return json.dumps(extracted_data), sectors_names, sectors_ids

    except Exception as e:
        log.exception("Failed to fetch PDS data for ID: %s", pds_id)
        raise AgentToolError(f"Failed to fetch PDS data: {e}") from e


def get_rooms():
    try:
        token = asyncio.run(oauth_manager.get_access_token())
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{settings.springboot_healthcare_url}/api/v1/pathways-medicals-staff/onlyMySector"

        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        available_rooms, occupied_rooms = [], []

        for room in data:
            room_summary = room.get("roomSummaryDto", {})
            room_number = room_summary.get("roomNumber")
            room_type = room_summary.get("roomType")

            if room_type == "SIMPLE":
                room_bed = room_number
            else:
                bed = room_summary.get("bed")
                if bed == "A":
                    bed = "P"
                elif bed == "B":
                    bed = "F"
                room_bed = f"{room_number}{bed}"

            pathway = room.get("pathwayDto")
            if pathway is None:
                available_rooms.append(room_bed)
            else:
                invitation_dto = pathway.get("invitationDto", {})
                lastname = invitation_dto.get("lastname", "not_found")
                firstname = invitation_dto.get("firstname", "not_found")
                patient_id = pathway.get("patientId", "not_found")
                pathway_name = pathway.get("pathwayType", {}).get("name", "not_found")
                occupied_rooms.append(f"{room_bed} : {lastname} {firstname} : {patient_id} : {pathway_name}")

        return available_rooms, occupied_rooms

    except Exception as e:
        log.exception("Failed to fetch rooms")
        raise AgentToolError(f"Failed to fetch rooms: {e}") from e


def get_planned_entries(hr_id):
    try:
        token = asyncio.run(oauth_manager.get_access_token())
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{settings.springboot_healthcare_url}/api/v1/planned-entries/today"
        params = {"id": hr_id}

        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            entries = response.json()

        filtered_entries = []
        for entry in entries:
            invitation = entry.get("invitationDto")
            if invitation:
                firstname = invitation.get("firstname", "")
                lastname = invitation.get("lastname", "")
                fullname = f"{firstname} {lastname}".strip()
                filtered_entries.append({
                    "fullname": fullname,
                    "service": entry.get("service"),
                    "entryDate": entry.get("entryDate")
                })

        return filtered_entries

    except Exception as e:
        log.exception("Failed to fetch planned entries for HR ID: %s", hr_id)
        raise AgentToolError(f"Failed to fetch planned entries: {e}") from e

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
        token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJlbW90d2lAeW9wbWFpbC5jb20iLCJzY29wZSI6WyJFYXN5bXMiXSwiZXhwIjoxNzYxMjM4NTMxLCJwZXJpbWV0ZXJzIjpbIjEiXSwiYXV0aG9yaXRpZXMiOlsiUEVSTV9DUkVBVEVfUEFUSFdBWSIsIlBFUk1fR0VUX0FTU0VTU01FTlQiLCJQRVJNX0NSRUFURV9QQVRJRU5UIiwiUEVSTV9HRVRfUEFUSFdBWSIsIlBFUk1fQ1JFQVRFX0lOVklUQVRJT04iLCJQRVJNX01PRElGWV9QQVRIV0FZIiwiUk9MRV9NRURJQ0FMX1NUQUZGIiwiUEVSTV9DUkVBVEVfVFJFQVRNRU5UIiwiUEVSTV9NT0RJRllfVFJFQVRNRU5UIiwiUEVSTV9HRVRfREVQQVJUTUVOVCIsIlBFUk1fR0VUX1RSRUFUTUVOVF9UWVBFIiwiUEVSTV9NT0RJRllfUEFUSUVOVCIsIlBFUk1fTU9ESUZZX0lOVklUQVRJT04iLCJQRVJNX0dFVF9QQVRIV0FZX1RZUEUiLCJQRVJNX0dFVF9QQVRJRU5UIiwiUEVSTV9HRVRfUk9PTSIsIlBFUk1fR0VUX0lOVklUQVRJT04iLCJQRVJNX0dFVF9UUkVBVE1FTlQiXSwianRpIjoiYzI0ZmZiZDQtNzZlZC00MTgwLThkN2UtOTdkNzkxMWExOTg1IiwiY2xpZW50X2lkIjoicGxhdGZvcm0tdWkifQ.giaikHPxNsRh3GjrpbYCnJjSmHxCWT_wnTo9BzbQKMm90F7KLK9ABOkycbnJcZZX_CKS-JpziLuOmlb6B8InoLU1jyEMgavYK5WDjxLgr52wYYzdael74xCXl1jp98aQT1P5JzDgI6c7oxbKcN8Lm-gJyxVmm3_kOF4QJb7mkkN38wAgHX1opvPewUzK4t_-_r1HGKQP1ON1iERi-l7IBRQCeUVEyFQiZlKIurjcUix36TvlKWvHX63BASPC3J-UA6Jc5jodgEo2BSxnh1i65deezXHACrZ8Oi4ofpMrRjmEQD3QX8ACGweKkftYTs9HKIvN3CGYFtM_WBRPjmYHOw"
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
        token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJlbW90d2lAeW9wbWFpbC5jb20iLCJzY29wZSI6WyJFYXN5bXMiXSwiZXhwIjoxNzYxMjM4NTMxLCJwZXJpbWV0ZXJzIjpbIjEiXSwiYXV0aG9yaXRpZXMiOlsiUEVSTV9DUkVBVEVfUEFUSFdBWSIsIlBFUk1fR0VUX0FTU0VTU01FTlQiLCJQRVJNX0NSRUFURV9QQVRJRU5UIiwiUEVSTV9HRVRfUEFUSFdBWSIsIlBFUk1fQ1JFQVRFX0lOVklUQVRJT04iLCJQRVJNX01PRElGWV9QQVRIV0FZIiwiUk9MRV9NRURJQ0FMX1NUQUZGIiwiUEVSTV9DUkVBVEVfVFJFQVRNRU5UIiwiUEVSTV9NT0RJRllfVFJFQVRNRU5UIiwiUEVSTV9HRVRfREVQQVJUTUVOVCIsIlBFUk1fR0VUX1RSRUFUTUVOVF9UWVBFIiwiUEVSTV9NT0RJRllfUEFUSUVOVCIsIlBFUk1fTU9ESUZZX0lOVklUQVRJT04iLCJQRVJNX0dFVF9QQVRIV0FZX1RZUEUiLCJQRVJNX0dFVF9QQVRJRU5UIiwiUEVSTV9HRVRfUk9PTSIsIlBFUk1fR0VUX0lOVklUQVRJT04iLCJQRVJNX0dFVF9UUkVBVE1FTlQiXSwianRpIjoiYzI0ZmZiZDQtNzZlZC00MTgwLThkN2UtOTdkNzkxMWExOTg1IiwiY2xpZW50X2lkIjoicGxhdGZvcm0tdWkifQ.giaikHPxNsRh3GjrpbYCnJjSmHxCWT_wnTo9BzbQKMm90F7KLK9ABOkycbnJcZZX_CKS-JpziLuOmlb6B8InoLU1jyEMgavYK5WDjxLgr52wYYzdael74xCXl1jp98aQT1P5JzDgI6c7oxbKcN8Lm-gJyxVmm3_kOF4QJb7mkkN38wAgHX1opvPewUzK4t_-_r1HGKQP1ON1iERi-l7IBRQCeUVEyFQiZlKIurjcUix36TvlKWvHX63BASPC3J-UA6Jc5jodgEo2BSxnh1i65deezXHACrZ8Oi4ofpMrRjmEQD3QX8ACGweKkftYTs9HKIvN3CGYFtM_WBRPjmYHOw"
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
        token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJFYXN5bXMiXSwiZXhwIjoxNzYxMjM4NTAwLCJhdXRob3JpdGllcyI6WyJST0xFX1BMQVRGT1JNX1VJIiwiUEVSTV9HRVRfUEFUSUVOVCIsIlBFUk1fQ1JFQVRFX01FRElDQUxfU1RBRkYiLCJST0xFX0RFQ09OTkVDVEVEVVNFUiJdLCJqdGkiOiIzMjJmZTU0MC03MDVlLTQzMTYtOWI5My1jNjA0ZjJhZjk2NGYiLCJjbGllbnRfaWQiOiJwbGF0Zm9ybS11aSJ9.c1IHAln5pryb6166Rl7sXOzATDjq3MvxHNlJHm1_4NlpsfYefrdyz-y9VF7I2MdJmxOhAwtHbDT5IntTlrhS9ukYVFDdPkWe7_KmwaWgQ6uVXw3wyKjTiJj1eE9nixBOwYkRkYOcclaKWUFEWU9w2xtNL1UThT9mJ7gQ5aEr6jvLI0VAA3fxL_ZJu1ocPVolveAhtC3yZVInQ-drtslxl8EjmvbItErUYQURruabLr4w2koxESKgdhkM36SIs23xBnmS4bdx5z85KannQIzzIfO9dmrk8Mu-Z4XmmB4laF1z5viMzGjf4SjJskYzO4fPbEbkaFsbDntEGTUc4uT_-A"
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

# agent_core/tools/get_pds.py
import httpx
from langchain.tools import tool
from agent_core.utils.logger import log
from agent_core.config.settings import settings
from agent_core.utils.exceptions import AgentToolError
from agent_core.utils.oauth import oauth_manager


@tool("get_pds_contact", return_direct=False)
async def get_pds_contact(input_data):
    """
    Récupère les coordonnées professionnelles d’un professionnel de santé (PDS)
    à partir de son prénom et nom de famille exacts.

    Args :
        input_data: dictionnaire avec les clés "firstname" and "lastname"
    """
    firstname = input_data.get("firstname")
    lastname = input_data.get("lastname")
    if not firstname or not lastname:
        raise AgentToolError("Missing 'firstname' or 'lastname' in input_data")

    log.info("Fetching PDS contact for: %s %s", firstname, lastname)

    try:
        token = await oauth_manager.get_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{settings.springboot_healthcare_facility_url}/api/v1/medical-staff?firstname={firstname}&lastname={lastname}"

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        matched_pds = []
        for pds in data:
            account = pds.get("account", {})
            matched_pds.append(
                {
                    "pdsId": pds.get("id"),
                    "pdsEmail": account.get("email"),
                    "pdsPhoneNumber": account.get("phoneNumber"),
                }
            )

        return matched_pds

    except httpx.HTTPStatusError as e:
        log.error(
            "HTTP error while fetching PDS contact for %s %s: %s",
            firstname, lastname, str(e)
        )
        raise AgentToolError(f"Failed to fetch PDS contact: {e}") from e
    except httpx.RequestError as e:
        log.error(
            "Request error while fetching PDS contact for %s %s: %s",
            firstname, lastname, str(e)
        )
        raise AgentToolError(f"Network error: {e}") from e
    except Exception as e:
        log.exception("Unexpected error fetching PDS contact for %s %s", firstname, lastname)
        raise AgentToolError(f"Unexpected error: {e}") from e

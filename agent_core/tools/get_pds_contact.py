# agent_core/tools/get_pds_contact.py
import asyncio, httpx
from langchain_core.tools import StructuredTool
from agent_core.utils.logger import log
from agent_core.config.settings import settings
from agent_core.utils.exceptions import AgentToolError
from agent_core.utils.oauth import oauth_manager


def fetch_pds_contact(firstname, lastname):
    try:
        token = asyncio.run(oauth_manager.get_access_token())
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{settings.springboot_healthcare_facility_url}/api/v1/medical-staff?firstname={firstname}&lastname={lastname}"

        with httpx.Client(timeout=10) as client:
            response = client.get(url, headers=headers)
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

    except Exception as e:
        log.exception("Unexpected error fetching PDS contact for %s %s", firstname, lastname)
        raise AgentToolError(f"Unexpected error: {e}") from e


get_pds_contact_tool = StructuredTool.from_function(
    func=fetch_pds_contact,
    name="get_pds_contact",
    description="Récupère les coordonnées professionnelles d’un PDS à partir de son prénom et nom de famille exacts.",
    input_schema={"type": "object", "properties": {
        "firstname": {"type": "string", "description": "Prénom exact du PDS"},
        "lastname": {"type": "string", "description": "Nom de famille exact du PDS"}
    }, "required": ["firstname", "lastname"]}
)

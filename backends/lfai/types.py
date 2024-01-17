from pydantic import BaseModel

##########
# RAG/VECTORDB
##########

class FilesByURLRequest(BaseModel):
    urls: list
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "urls": [
                        "https://adlnet.gov/assets/uploads/webinars/DevSecOps%20and%20LTW%20Webinar%20Slides_Weiss-Smith-Udell.pdf",
                        "https://dodcio.defense.gov/Portals/0/Documents/DoD%20Enterprise%20DevSecOps%20Reference%20Design%20v1.0_Public%20Release.pdf",
                        "https://dodcio.defense.gov/Portals/0/Documents/Library/DoDEnterpriseDevSecOpsFundamentals.pdf",
                    ]
                }
            ]
        }
    }


class Query(BaseModel):
    query: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "how can one mitigate and reduce risk?",
                },                
            ]
        }
    }


class URLRequest(BaseModel):
    # urls = ConfigDict(strict=False)
    urls: list
    extensions: list
    url_base: str
    limit: int
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "urls": ['https://read.84000.co/section/all-translated.html'],
                    "extensions": ['pdf'],
                    "url_base": "https://read.84000.co",
                    "limit": 3,
                },
            ]
        }
    }

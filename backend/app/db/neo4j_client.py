from neo4j import GraphDatabase
 
from app.core.config import settings
 
 
class Neo4jClient:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
 
    def close(self):
        self._driver.close()
 
    def verify_connection(self) -> bool:
        with self._driver.session() as session:
            result = session.run("RETURN 1 AS ok")
            return result.single()["ok"] == 1
 
    def run_query(self, query: str, params: dict | None = None):
        with self._driver.session() as session:
            return list(session.run(query, params or {}))
 
 
neo4j_client = Neo4jClient()

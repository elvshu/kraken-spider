from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    label: str
    host: str
    db_password: str
    db_user: str | None = None
    db_port: str | None = "5432"
    db_name: str | None = None
    local_env: str | None = None
    replica_host: str | None = None
    django_configuration: str | None = None

    @property
    def src(self) -> str:
        return os.path.join(os.path.join(os.path.expanduser("~"), "src"), self.local_env)

    def _db_generate(self) -> str:
        database_configs = [
            f'DATABASE_HOST="{self.host}"',
            f'DATABASE_REPLICA_HOST="{self.replica_host if self.replica_host else self.host}"',
            f'DATABASE_USER="{self.db_user}"',
            f'DATABASE_NAME="{self.db_name}"',
            f'DATABASE_PASSWORD="{self.db_password}"',
            f'DATABASE_PORT="{self.db_port}"',
        ]
        return " ".join(database_configs)

    def generate(self) -> str:
        alias = f"alias {self.label}='workon {self.local_env}; "
        if self.django_configuration:
            alias += f"DJANGO_CONFIGURATION={self.django_configuration} "
        return alias + self._db_generate() + f" python {self.src}/src/manage.py shell'"


class Kraken(Config):
    def __init__(self, *args, **kwargs) -> None:
        configurations = {
            "origin": "OriginSupportSite",
            "ergon": "ErgonSupportSite",
            "nectr": "NectrSupportSite"
        }
        kwargs.update({
            "local_env": "kraken-core",
            "db_name": "krakencore",
            "db_user": kwargs.get("db_user", "internal_reporter"),
            "django_configuration": configurations[kwargs["label"].split("_", 1)[0]]
        })
        super().__init__(*args, **kwargs)


class Chroma(Config):
    def __init__(self, *args, **kwargs) -> None:
        db_users = {
            "origin": "chroma_support"
        }
        kwargs.update(
            {
                "local_env": "aus-sdr",
                "db_name": "main",
                "db_user": db_users.get(kwargs["label"].split("_", 1)[0], "internal-reporting")
            }
        )
        super().__init__(*args, **kwargs)


configs = [
    Kraken(label="origin_kraken_prod", host="postgres-analytics-replica.origin.prod.kraken.internal", db_password="465216df-aef8-40b9-ad7b-9a8d45b739e0"),
    Chroma(label="origin_chroma_prod", host="chroma-db-ro.int.origin-kraken.energy", db_password="ec99751a-cbc5-47a9-81de-ea2ef59bda96"),
    Kraken(label="origin_kraken_test", host="postgres-analytics-replica.origin.test.kraken.internal", db_password="4f88a715-25ef-45d2-a9f4-abaff5f98977"),
    Chroma(label="origin_chroma_test", host="chroma-db-ro.int.origin-kraken.systems", db_password="4b5e1dd4-5b68-4d24-9068-41a92e64d6be"),
    Kraken(label="nectr_kraken_prod", host="postgres-analytics-replica.nectr.prod.kraken.internal", db_user="internal-reporting", db_password="DCC364C8-5E44-4A45-A469-5F27E67A361B"),
    Chroma(label="nectr_chroma_prod", host="chroma-db-ro.int.nectr-kraken.energy", db_password="7B269628-A2F9-4FD3-9F29-9190A2D05C13"),
    Kraken(label="nectr_kraken_test", host="postgres-comms.nectr.test.kraken.internal", db_password="82f5aae6-0f95-4678-85e7-ce74d676716f"),
    Chroma(label="nectr_chroma_test", host="chroma-db-ro.int.nectr-kraken.systems", db_password="202EB0D3-CD27-4FFF-8F9B-AA5A5F4822DB"),
    Kraken(label="ergon_kraken_prod", host="postgres-analytics-replica.ergon.prod.kraken.internal", db_password="CHd7hnPWvEp6Ri93Paaq"),
    Chroma(label="ergon_chroma_prod", host="chroma-db-ro.int.ergon-kraken.energy", db_password="11922F40-45F1-485B-9756-68067AEA8989"),
    Kraken(label="ergon_kraken_test", host="postgres-analytics-replica.ergon.test.kraken.internal", db_password="RiLwNb6racPyiweQaNLo"),
    Chroma(label="ergon_chroma_test", host="chroma-db-ro.int.ergon-kraken.systems", db_password="A61472BA-188A-4CE7-8173-B33C60573068"),
]

if __name__ == "__main__":
    with open("alias", "w") as wf:
        for config in configs:
            wf.write(config.generate() + "\n")


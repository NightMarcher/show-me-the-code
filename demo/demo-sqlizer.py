from json import dumps
from typing import Any, Dict, List, Optional


class SQLizer:

    @staticmethod
    def wrap_backticks(identifier: str):
        assert isinstance(identifier, str), f"identifier({identifier}) must be instance of `str`"
        return f"`{str(identifier).strip('`')}`"

    @staticmethod
    def escape(obj, to_json=False):
        """
        Original DIY `escape` method
        """
        if obj is None:
            return "NULL"
        elif isinstance(obj, (int, float, bool)):
            return f"{obj}"
        elif isinstance(obj, (dict, list, tuple)):
            dumped = dumps(obj, ensure_ascii=False)
            if to_json:
                return f"CAST('{dumped}' AS JSON)"
                # Same with above line
                # return f"JSON_EXTRACT('{dumped}', '$')"
            return f"'{dumped}'"
        else:
            return f"'{obj}'"

    @classmethod
    def build_fly_table(
        cls,
        dicts: List[Dict[str, Any]],
        fields: List[str],
        using_values: bool = True,
    ) -> Optional[str]:
        if not all([dicts, fields]):
            raise Exception("Parameters `dicts`, `fields` are required")

        if using_values:
            rows = [
                f"          ROW({', '.join(cls.escape(d.get(f)) for f in fields)})"
                for d in dicts
            ]
            values = "VALUES\n" + ",\n".join(rows)
            table = f"fly_table ({', '.join(fields)})"
        else:
            rows = [
                f"SELECT {', '.join(f'{cls.escape(d.get(f))} {f}' for f in fields)}"
                for d in dicts
            ]
            values = "\n            UNION\n          ".join(rows)
            table = "fly_table"

        sql = f"""
        SELECT * FROM (
          {values}
        ) AS {table}"""
        return sql

    @classmethod
    def bulk_update_from_dicts(
        cls,
        table: str,
        dicts: List[Dict[str, Any]],
        join_fields: List[str],
        update_fields: List[str],
        *,
        merge_fields: Optional[List[str]] = None,
        using_values: bool = False,
    ) -> Optional[str]:
        if not all([table, dicts, join_fields, update_fields]):
            raise Exception("Parameters `table`, `dicts`, `join_fields`, `update_fields` are required")

        joins = [f"{cls.wrap_backticks(table)}.{jf}=tmp.{jf}" for jf in join_fields]
        updates = [f"{cls.wrap_backticks(table)}.{uf}=tmp.{uf}" for uf in update_fields]
        merge_fields = merge_fields or []
        for mf in merge_fields:
            dict_obj = f"IFNULL({cls.wrap_backticks(table)}.{mf}, '{{}}')"
            updates.append(f"{cls.wrap_backticks(table)}.{mf}=JSON_MERGE_PATCH({dict_obj}, tmp.{mf})")

        sql = f"""
    UPDATE {cls.wrap_backticks(table)}
    JOIN ({cls.build_fly_table(dicts, join_fields + update_fields + merge_fields, using_values)}
    ) tmp ON {" AND ".join(joins)}
    SET {", ".join(updates)}
"""
        return sql

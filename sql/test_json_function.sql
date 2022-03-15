CREATE OR REPLACE FUNCTION SCHEMA_NAME.test_json_function() RETURNS json LANGUAGE plpgsql AS $function$
DECLARE
    v_project_type text;
    v_version text;

BEGIN

    SELECT project_type, giswater INTO v_project_type, v_version FROM SCHEMA_NAME.sys_version ORDER BY id DESC LIMIT 1;

    --RAISE EXCEPTION 'Exception raised!!!';

    RETURN ('{"status":"Accepted", "message":{"level":0, "text":"Database function ''test_json_function'' executed successfully"}, "version":"'||v_version||'"'||
             ',"body":{"form":{}, "data":{"info":"INFO"}}}')::json;

END;
$function$

-- Example of Snowflake RBAC(Role-Based Access Control) setup for EU Energy Storage Platform

CREATE WAREHOUSE sales_analyst_wh
WAREHOUSE_SIZE = 'SMALL'
WAREHOUSE_TYPE = 'STANDARD'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE
MIN_CLUSTER_COUNT = 1
MAX_CLUSTER_COUNT = 1
SCALING_POLICY = 'STANDARD';

drop warehouse sales_analyst_wh

CREATE ROLE sales_analyst_role;


CREATE USER sales_analyst
PASSWORD = '1234'
LOGIN_NAME = 'sales_analyst_1'
DEFAULT_ROLE = 'sales_analyst_role'
DEFAULT_WAREHOUSE = 'sales_analyst_wh'
MUST_CHANGE_PASSWORD = FALSE;


CREATE WAREHOUSE risk_analyst_wh
WAREHOUSE_SIZE = 'SMALL'
WAREHOUSE_TYPE = 'STANDARD'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE
MIN_CLUSTER_COUNT = 1
MAX_CLUSTER_COUNT = 1
SCALING_POLICY = 'STANDARD';


CREATE ROLE risk_analyst_role;



CREATE USER risk_analyst
PASSWORD = '1234'
LOGIN_NAME = 'risk_analyst_1'
DEFAULT_ROLE = 'risk_analyst_role'
DEFAULT_WAREHOUSE = 'risk_analyst_wh'
MUST_CHANGE_PASSWORD = FALSE;


CREATE WAREHOUSE ml_ai_team_wh
WAREHOUSE_SIZE = 'MEDIUM'
WAREHOUSE_TYPE = 'STANDARD'
AUTO_SUSPEND = 300
AUTO_RESUME = TRUE
MIN_CLUSTER_COUNT = 1
MAX_CLUSTER_COUNT = 1
SCALING_POLICY = 'STANDARD';


CREATE ROLE ml_ai_team_role;


CREATE USER ml_ai_team
PASSWORD = '1234'
LOGIN_NAME = 'ml_ai_team_1'
DEFAULT_ROLE = 'ml_ai_team_role'
DEFAULT_WAREHOUSE = 'ml_ai_team_wh'
MUST_CHANGE_PASSWORD = FALSE;


GRANT USAGE ON WAREHOUSE sales_analyst_wh TO ROLE sales_analyst_role;
GRANT ROLE sales_analyst_role TO USER sales_analyst;

GRANT USAGE ON WAREHOUSE risk_analyst_wh TO ROLE risk_analyst_role;
GRANT ROLE risk_analyst_role TO USER risk_analyst;

GRANT USAGE ON WAREHOUSE ml_ai_team_wh TO ROLE ml_ai_team_role;
GRANT ROLE ml_ai_team_role TO USER ml_ai_team;

-- Database access
GRANT USAGE ON DATABASE EU_ENERGY_DB TO ROLE sales_analyst_role;
GRANT USAGE ON DATABASE EU_ENERGY_DB TO ROLE risk_analyst_role;
GRANT USAGE ON DATABASE EU_ENERGY_DB TO ROLE ml_ai_team_role;

-- Schema access
GRANT USAGE ON SCHEMA EU_ENERGY_DB.ANALYTICS TO ROLE sales_analyst_role;
GRANT USAGE ON SCHEMA EU_ENERGY_DB.ANALYTICS TO ROLE risk_analyst_role;
GRANT USAGE ON SCHEMA EU_ENERGY_DB.ANALYTICS TO ROLE ml_ai_team_role;



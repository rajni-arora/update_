I have 

Configs-

sqlgen:
    usecase: [“cru”, “sabe”]

So in the first image i want usecase shoulbe replace 2 times one for cru then for sabe

We need to make changes in the 2nd image on the code

Please write a logic

Code should work like
It will work for cru then do the work like read and write of the data
The work for Sabe 



def read_config_set_env(app):
    app_env = os.getenv('EPAAS_ENV')
    env_config_path = f"configs/{app_env}_config.yml"
    os.environ["CONFIG_PATH"] = env_config_path

    common_config = load_config('configs/config.yml')
    dialect = common_config['sqlgen']['dialect'].lower()

    # -----------------------------
    # NEW: Handle multiple usecases
    # -----------------------------
    usecases = common_config['sqlgen']['usecase']   # this is a list: ["cru", "sabe"]
    combined_configs = []  # store config for every usecase separately

    for usecase in usecases:
        usecase = usecase.lower()

        # --- Build S3 paths ---
        s3_file_paths = common_config['s3_file_paths']
        updated_s3_paths = {}
        for key, val in s3_file_paths.items():
            new_path = val.replace('{dialect}', dialect).replace('{usecase}', usecase)
            updated_s3_paths[key] = new_path

        # --- Build local paths ---
        local_file_paths = common_config['local_file_paths']
        updated_local_paths = {}
        for key, val in local_file_paths.items():
            new_path = val.replace('{dialect}', dialect).replace('{usecase}', usecase)
            updated_local_paths[key] = new_path

        # Load env config
        env_config = load_config(env_config_path)

        # Combine config
        usecase_config = {
            **common_config,
            **env_config,
            "s3_file_paths": updated_s3_paths,
            "local_file_paths": updated_local_paths,
            "usecase": usecase
        }

        combined_configs.append(usecase_config)

    # Return list of configs → caller will process each
    app.state.config = combined_configs
    return combined_configs
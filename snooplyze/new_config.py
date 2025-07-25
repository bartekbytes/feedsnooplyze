from configuration.config_new import load_config

if __name__ == "__main__":
    general_cfg, persistence_cfg, notifications = load_config("../config copy.yaml")
    print(general_cfg)
    print(persistence_cfg)
    for n in notifications:
        print(n)

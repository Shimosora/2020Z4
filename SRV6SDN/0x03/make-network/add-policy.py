import subprocess
import yaml
import pprint

def ensure_rule(rule):
    # TODO: KOKO_NI_NANIKA_WO_KAKU!!
    c0 = ["ip", "netns", "exec"]
    src = rule["target_src"]
    dst = rule["target_dst"]
    tab = rule["id"]
    slu = rule["functions"] 
    sld = rule["functions"]

    subprocess.run(c0 + ["R1", "ip", "rule", "add", "prio", tab, 
                         "from", src, "to", dst, "table", tab])
    subprocess.run(c0 + ["R2", "ip", "rule", "add", "prio", tab, 
                         "from", dst, "to", src, "table", tab])
    
    if len(rule["functions"]) == 2:
        subprocess.run(c0 + ["R1", "ip", "route", "add", "{}/32".format(dst), 
                         "encap", "seg6", "mode", "encap", "segs", 
                         "{},{},F2::10".format(slu[0],slu[1]), "dev", "net2", "table", tab])

        subprocess.run(c0 + ["R2", "ip", "route", "add", "{}/32".format(src), 
                         "encap", "seg6", "mode", "encap", "segs", 
                         "{},{},F1::10".format(sld[1],slu[0]), "dev", "net2", "table", tab])

    elif len(rule["functions"]) == 3:
        subprocess.run(c0 + ["R1", "ip", "route", "add", "{}/32".format(dst), 
                         "encap", "seg6", "mode", "encap", "segs", 
                         "{},{},{},F2::10".format(slu[0],slu[1],slu[2]), "dev", "net2", "table", tab])

        subprocess.run(c0 + ["R2", "ip", "route", "add", "{}/32".format(src), 
                         "encap", "seg6", "mode", "encap", "segs", 
                         "{},{},{},F1::10".format(sld[2],sld[1],slu[0]), "dev", "net2", "table", tab])



def main():

    config = {}
    with open("./policy.yml") as yml:
        config = yaml.load(yml, Loader=yaml.SafeLoader)

    pprint.pprint(config)

    for rule in config["rules"]:
        ensure_rule(rule)
    #- id: 100
    #  target_src: 10.1.0.11 #C1
    #  target_dst: 10.2.0.14 #C4
    #  functions: [FF:1::1, FF:2::1]
   # rule = {}
   # rule["id"] = "100"
   # rule["target_src"] = "10.1.0.11"
   # rule["target_dst"] = "10.2.0.14"
   # rule["functions"] = ["FF:1::1", "FF:2::1"]
   # ensure_rule(rule)

   # #- id: 200
   # #  target_src: 10.1.0.11 #C1
   # #  target_dst: 10.2.0.15 #C5
   # #  functions: [FF:2::1, FF:3::1, FF:1::1]
   # rule["id"] = "200"
   # rule["target_src"] = "10.1.0.11"
   # rule["target_dst"] = "10.2.0.15"
   # rule["functions"] = ["FF:2::1", "FF:3::1","FF:1::1"]
   # ensure_rule(rule)
   # 
   # #- id: 300
   # # target_src: 10.1.0.11 #C1
   # # target_dst: 10.2.0.16 #C6
   # # functions: [FF:1::1,FF:2::1]
   # 
   # rule["id"] = "300"
   # rule["target_src"] = "10.1.0.11"
   # rule["target_dst"] = "10.2.0.16"
   # rule["functions"] = ["FF:1::1","FF:2::1"]
   # ensure_rule(rule) 

if __name__ == '__main__':
    main()


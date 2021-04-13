import json
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables


macIDs = {"platformID": 3, "platEncID": 1, "langID": 0x409}


def add_feature_names(font_path, feature_names_path):

    with open(feature_names_path, "r") as f:
        feature_names = json.load(f)

    font = TTFont(font_path)
    table_name = font["name"]
    table_gsub = font["GSUB"].table

    feature_names_ids = {}
    max_id = max(name.nameID for name in table_name.names)
    id = 256 if max_id < 256 else max_id + 1
    for tag, feature_name in feature_names.items():
        table_name.setName(feature_name, id, *macIDs.values())
        feature_names_ids[tag] = id
        id += 1

    for featureRecord in table_gsub.FeatureList.FeatureRecord:
        tag = featureRecord.FeatureTag
        if tag in feature_names:
            params = otTables.FeatureParamsStylisticSet()
            params.Version = 0
            params.UINameID = feature_names_ids[tag]
            featureRecord.Feature.FeatureParams = params

    parts = font_path.split(".")
    font.save(".".join(parts[:-1]) + "1." + parts[-1])


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("font_path")
    parser.add_argument("feature_names_path")

    args = parser.parse_args()

    add_feature_names(args.font_path, args.feature_names_path)
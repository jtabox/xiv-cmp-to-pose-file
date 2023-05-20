# Converts .cmp files to .pose files (Pose files are used by Anamnesis/Ktisis in FFXIV)
# Used the code from https://xivposeconverter.netlify.app/ and converted it to Python
# Couldn't find the code's author to mention by name, so thank you to whoever wrote it :)

# Explanation of the conversion process, courtesy of my precious GPT-4:
# (Btw the rotation data for each bone is 4 values which is in quaternion format)
#
# 1. Read the .cmp file and extract the relevant information, such as the bone name and its associated values:
# ("Waist": "DB C4 32 3F F3 E6 9B BE 4B 8E 15 3F 05 4F 8F BE")
# 2. Remove spaces from the given bone data:
# ("Waist": "DBC4323FF3E69BBE4B8E153F054F8FBF")
# 3. Split the data into 8-character groups:
# ("Waist": ["DBC4323F", "F3E69BBE", "4B8E153F", "054F8FBF"])
# 4. Reverse the byte order of each group (function reverse_byte_order below):
# ("Waist": ["3F32C4DB", "BE9BE6F3", "3F158E4B", "BF8F4F05"])
# 5. Convert each group to a float (function convert_hex_to_float below):
# ("Waist": ["0.79710668", "-0.18765971", "0.57154870", "-0.11197264"])
# 6. Negate each floating point value:
# ("Waist": ["-0.79710668", "0.18765971", "-0.57154870", "0.11197264"])
#
# Now we have the converted rotation values for the bone, which is what we want, since apparently the "Position"
# and "Scale" values are changed to "0, 0, 0" and "1, 1, 1" respectively in the .pose data, and supposedly it works.
# The rest is just converting the bone name using the conversion table below, and formatting all the data together
# into JSON format for the .pose file.

import json


def reverse_byte_order(input_str, count):
    # Function for step 4 in the conversion process above
    result = input_str[:2]
    for i in range(count):
        result += input_str[2 + (count - 1 - i) * 2: 2 + (count - 1 - i) * 2 + 2]
    return result


def convert_hex_to_float(num):
    # Function for step 5 in the conversion process above
    sign = -1 if (num >> 31) else 1
    exponent = (num >> 23) & 255
    return sign * (num & 8388607 | 8388608) * 1 / pow(2, 23) * pow(2, exponent - 127)


def convert_cmp_to_pose(data):
    # The main function that converts .cmp data to .pose data
    conversion_table = {
        "Root": "n_root",
        "Abdomen": "n_hara",
        "Throw": "n_throw",
        "Waist": "j_kosi",
        "SpineA": "j_sebo_a",
        "LegLeft": "j_asi_a_l",
        "LegRight": "j_asi_a_r",
        "HolsterLeft": "j_buki2_kosi_l",
        "HolsterRight": "j_buki2_kosi_r",
        "SheatheLeft": "j_buki_kosi_l",
        "SheatheRight": "j_buki_kosi_r",
        "SpineB": "j_sebo_b",
        "ClothBackALeft": "j_sk_b_a_l",
        "ClothBackARight": "j_sk_b_a_r",
        "ClothFrontALeft": "j_sk_f_a_l",
        "ClothFrontARight": "j_sk_f_a_r",
        "ClothSideALeft": "j_sk_s_a_l",
        "ClothSideARight": "j_sk_s_a_r",
        "KneeLeft": "j_asi_b_l",
        "KneeRight": "j_asi_b_r",
        "BreastLeft": "j_mune_l",
        "BreastRight": "j_mune_r",
        "SpineC": "j_sebo_c",
        "ClothBackBLeft": "j_sk_b_b_l",
        "ClothBackBRight": "j_sk_b_b_r",
        "ClothFrontBLeft": "j_sk_f_b_l",
        "ClothFrontBRight": "j_sk_f_b_r",
        "ClothSideBLeft": "j_sk_s_b_l",
        "ClothSideBRight": "j_sk_s_b_r",
        "CalfLeft": "j_asi_c_l",
        "CalfRight": "j_asi_c_r",
        "ScabbardLeft": "j_buki_sebo_l",
        "ScabbardRight": "j_buki_sebo_r",
        "Neck": "j_kubi",
        "ClavicleLeft": "j_sako_l",
        "ClavicleRight": "j_sako_r",
        "ClothBackCLeft": "j_sk_b_c_l",
        "ClothBackCRight": "j_sk_b_c_r",
        "ClothFrontCLeft": "j_sk_f_c_l",
        "ClothFrontCRight": "j_sk_f_c_r",
        "ClothSideCLeft": "j_sk_s_c_l",
        "ClothSideCRight": "j_sk_s_c_r",
        "PoleynLeft": "n_hizasoubi_l",
        "PoleynRight": "n_hizasoubi_r",
        "FootLeft": "j_asi_d_l",
        "FootRight": "j_asi_d_r",
        "Head": "j_kao",
        "ArmLeft": "j_ude_a_l",
        "ArmRight": "j_ude_a_r",
        "PauldronLeft": "n_kataarmor_l",
        "PauldronRight": "n_kataarmor_r",
        "ToesLeft": "j_asi_e_l",
        "ToesRight": "j_asi_e_r",
        "HairA": "j_kami_a",
        "HairFrontLeft": "j_kami_f_l",
        "HairFrontRight": "j_kami_f_r",
        "EarLeft": "j_mimi_l",
        "EarRight": "j_mimi_r",
        "ForearmLeft": "j_ude_b_l",
        "ForearmRight": "j_ude_b_r",
        "ShoulderLeft": "n_hkata_l",
        "ShoulderRight": "n_hkata_r",
        "HairB": "j_kami_b",
        "HandLeft": "j_te_l",
        "HandRight": "j_te_r",
        "ShieldLeft": "n_buki_tate_l",
        "ShieldRight": "n_buki_tate_r",
        "EarringALeft": "n_ear_a_l",
        "EarringARight": "n_ear_a_r",
        "ElbowLeft": "n_hhiji_l",
        "ElbowRight": "n_hhiji_r",
        "CouterLeft": "n_hijisoubi_l",
        "CouterRight": "n_hijisoubi_r",
        "WristLeft": "n_hte_l",
        "WristRight": "n_hte_r",
        "IndexALeft": "j_hito_a_l",
        "IndexARight": "j_hito_a_r",
        "PinkyALeft": "j_ko_a_l",
        "PinkyARight": "j_ko_a_r",
        "RingALeft": "j_kusu_a_l",
        "RingARight": "j_kusu_a_r",
        "MiddleALeft": "j_naka_a_l",
        "MiddleARight": "j_naka_a_r",
        "ThumbALeft": "j_oya_a_l",
        "ThumbARight": "j_oya_a_r",
        "WeaponLeft": "n_buki_l",
        "WeaponRight": "n_buki_r",
        "EarringBLeft": "n_ear_b_l",
        "EarringBRight": "n_ear_b_r",
        "IndexBLeft": "j_hito_b_l",
        "IndexBRight": "j_hito_b_r",
        "PinkyBLeft": "j_ko_b_l",
        "PinkyBRight": "j_ko_b_r",
        "RingBLeft": "j_kusu_b_l",
        "RingBRight": "j_kusu_b_r",
        "MiddleBLeft": "j_naka_b_l",
        "MiddleBRight": "j_naka_b_r",
        "ThumbBLeft": "j_oya_b_l",
        "ThumbBRight": "j_oya_b_r",
        "TailA": "n_sippo_a",
        "TailB": "n_sippo_b",
        "TailC": "n_sippo_c",
        "TailD": "n_sippo_d",
        "TailE": "n_sippo_e",
        "RootHead": "j_kao",
        "Jaw": "j_ago",
        "EyelidLowerLeft": "j_f_dmab_l",
        "EyelidLowerRight": "j_f_dmab_r",
        "EyeLeft": "j_f_eye_l",
        "EyeRight": "j_f_eye_r",
        "Nose": "j_f_hana",
        "CheekLeft": "j_f_hoho_l",
        "CheekRight": "j_f_hoho_r",
        "LipsLeft": "j_f_lip_l",
        "LipsRight": "j_f_lip_r",
        "EyebrowLeft": "j_f_mayu_l",
        "EyebrowRight": "j_f_mayu_r",
        "Bridge": "j_f_memoto",
        "BrowLeft": "j_f_miken_l",
        "BrowRight": "j_f_miken_r",
        "LipUpperA": "j_f_ulip_a",
        "EyelidUpperLeft": "j_f_umab_l",
        "EyelidUpperRight": "j_f_umab_r",
        "LipLowerA": "j_f_dlip_a",
        "LipUpperB": "j_f_ulip_b",
        "LipLowerB": "j_f_dlip_b",
        "VieraEar01ALeft": "j_zera_a_l",
        "VieraEar01ARight": "j_zera_a_r",
        "VieraEar01BLeft": "j_zera_b_l",
        "VieraEar01BRight": "j_zera_b_r",
        "VieraEar02ALeft": "j_zerb_a_l",
        "VieraEar02ARight": "j_zerb_a_r",
        "VieraEar02BLeft": "j_zerb_b_l",
        "VieraEar02BRight": "j_zerb_b_r",
        "VieraEar03ALeft": "j_zerc_a_l",
        "VieraEar03ARight": "j_zerc_a_r",
        "VieraEar03BLeft": "j_zerc_b_l",
        "VieraEar03BRight": "j_zerc_b_r",
        "VieraEar04ALeft": "j_zerd_a_l",
        "VieraEar04ARight": "j_zerd_a_r",
        "VieraEar04BLeft": "j_zerd_b_l",
        "VieraEar04BRight": "j_zerd_b_r",
        "VieraLipLowerA": "j_f_dlip_a",
        "VieraLipUpperB": "j_f_ulip_b",
        "VieraLipLowerB": "j_f_dlip_b",
        "HrothWhiskersLeft": "j_f_hige_l",
        "HrothWhiskersRight": "j_f_hige_r",
        "HrothEyebrowLeft": "j_f_mayu_l",
        "HrothEyebrowRight": "j_f_mayu_r",
        "HrothBridge": "j_f_memoto",
        "HrothBrowLeft": "j_f_miken_l",
        "HrothBrowRight": "j_f_miken_r",
        "HrothJawUpper": "j_f_uago",
        "HrothLipUpper": "j_f_ulip",
        "HrothEyelidUpperLeft": "j_f_umab_l",
        "HrothEyelidUpperRight": "j_f_umab_r",
        "HrothLipsLeft": "n_f_lip_l",
        "HrothLipsRight": "n_f_lip_r",
        "HrothLipUpperLeft": "n_f_ulip_l",
        "HrothLipUpperRight": "n_f_ulip_r",
        "HrothLipLower": "j_f_dlip"
    }

    # Start creating the resulting pose string
    converted_pose_data = {
        "FileExtension": ".pose",
        "TypeName": "Anamnesis Pose",
        "Position": "0, 0, 0",
        "Rotation": "0, 0, 0, 1",
        "Scale": "1, 1, 1",
        "Bones": {},
        "Author": "CMP to POSE file converter",
    }

    # Go through each key-value pair in the cmp data and convert them to pose data
    for key, value in data.items():
        # Those keys do not exist in pose files, skipping them
        if any(term in key for term in ["Size", "Description", "DateCreated", "CMPVersion", "Race", "Clan",
                                        "Body"]) or key not in conversion_table or value is None or value == "null":
            continue

        # Get the correct bone name
        bone_name = conversion_table[key]

        # Convert the rotation data from a hexadecimal string to 4 floats and back to a string
        rotation_data = value.replace(" ", "")
        groups = [rotation_data[i:i + 8] for i in range(0, len(rotation_data), 8)]
        groups = [round(float(convert_hex_to_float(int(reverse_byte_order("0x" + group, 8), 16))), 8) for group in
                  groups]
        groups = [-group for group in groups]
        rotation_str = ", ".join(str(group) for group in groups)

        # Create a JSON entry with the converted data
        converted_pose_data["Bones"][bone_name] = {
            "Position": "0, 0, 0",
            "Rotation": rotation_str,
            "Scale": "1, 1, 1"
        }
    return converted_pose_data


# Reading the .cmp file
with open("input_file.cmp", "r") as infile:
    cmp_data = json.load(infile)

# Converting .cmp to .pose
pose_data = convert_cmp_to_pose(cmp_data)

# Writing the .pose file
with open("output_file.pose", "w") as outfile:
    json.dump(pose_data, outfile, indent=4)

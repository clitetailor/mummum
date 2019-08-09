# *-* coding: utf-8 *-*
from pymongo import MongoClient

client = MongoClient()
db = client['lunch']
Users = db['users']
Booking = db['booking']
Menu = db['menu']
Payed = db['payed']
PayedHTUD = db['htud']
LuckyGuys = db['luckyguys']
data_lst = [
    {
        "day": "Monday",
        "Menu": [
            {
                "path": "Monday/bo_sot_vang.jpg",
                "price": "40",
                "name": "Bò sốt vang",
                "code": "1"
            },
            {
                "path": "Monday/canh_ga_chien_mam.jpg",
                "price": "35",
                "name": "Cánh gà chiên mắm",
                "code": "2"
            },
            {
                "path": "Monday/chan_gio_hap_xa.jpg",
                "price": "35",
                "name": "Chân giò hấp xả",
                "code": "3"
            },
            {
                "path": "Monday/suon_chu_ngot.jpg",
                "price": "35",
                "name": "Sườn xào chua ngọt",
                "code": "4"
            }
        ]
    },
    {
        "day": "Tuesday",
        "Menu": [
            {
                "path": "Tuesday/ca_com_tuoi_chien.jpg",
                "price": "40",
                "name": "Cá cơm tươi chiên vàng",
                "code": "1"
            },
            {
                "path": "Tuesday/suon_dim_tieu_large.jpg",
                "price": "35",
                "name": "Sườn lợn rim tiêu",
                "code": "2"
            },
            {
                "path": "Tuesday/thit_kho_tau.jpg",
                "price": "35",
                "name": "Thịt kho tàu",
                "code": "3"
            },
            {
                "path": "Tuesday/tom_rang_thit_ba_chi_large.jpg",
                "price": "35",
                "name": "Tôm rang thịt ba chỉ",
                "code": "4"
            },
            {
                "path": "Tuesday/com_dui_ga_w_large.jpg",
                "price": "45",
                "name": "Cơm đùi gà sốt BBQ",
                "code": "5"
            }
        ]
    },
    {
        "day": "Wednesday",
        "Menu": [
            {
                "path": "Wednesday/g___p_ch_o_large.jpg",
                "price": "35",
                "name": "Gà áp chảo",
                "code": "1"
            },
            {
                "path": "Wednesday/ga_ap_chao.jpg",
                "price": "35",
                "name": "Gà áp chảo",
                "code": "2"
            },
            {
                "path": "Wednesday/suon_rim_dua.jpg",
                "price": "35",
                "name": "Sườn rim dứa",
                "code": "3"
            },
            {
                "path": "Wednesday/thit_trung_mam_tep.jpg",
                "price": "35",
                "name": "Thịt trưng mắm tép",
                "code": "4"
            }
        ]
    },
    {
        "day": "Thursday",
        "Menu": [
            {
                "path": "Thursday/suon_chu_ngot_large",
                "price": "35",
                "name": "Sườn chua ngọt",
                "code": "1"
            },
            {
                "path": "Thursday/th_t_kho_d_a_large.jpg",
                "price": "35",
                "name": "Thịt kho dừa",
                "code": "2"
            },
            {
                "path": "Thursday/upload_1cba387545804c3aad47fc20ef9b2af2_large.jpg",
                "price": "35",
                "name": "Thăn lợn rim tiêu",
                "code": "3"
            },
            {
                "path": "Thursday/ga-kho-gung___large.jpg",
                "price": "35",
                "name": "Gà rang gừng",
                "code": "4"
            }
        ]
    },
    {
        "day": "Friday",
        "Menu": [
            {
                "path": "Friday/ca_kho_mang.jpg",
                "price": "40",
                "name": "Cá kho măng",
                "code": "1"
            },
            {
                "path": "Friday/ga_ap_chao.jpg",
                "price": "35",
                "name": "Gà áp chảo",
                "code": "2"
            },
            {
                "path": "Friday/suon_rim_dua.jpg",
                "price": "35",
                "name": "Sườn rim dứa",
                "code": "3"
            },
            {
                "path": "Friday/thit_trung_mam_tep.jpg",
                "price": "35",
                "name": "Thịt trưng mắm tép",
                "code": "4"
            }
        ]
    },
    {
        "day": "Saturday",
        "Menu": [
            {
                "path": "Saturday/ca_kho_mang.jpg",
                "price": "40",
                "name": "Cá kho măng",
                "code": "1"
            },
            {
                "path": "Saturday/ga_ap_chao.jpg",
                "price": "35",
                "name": "Gà áp chảo",
                "code": "2"
            },
            {
                "path": "Saturday/suon_rim_dua.jpg",
                "price": "35",
                "name": "Sườn rim dứa",
                "code": "3"
            },
            {
                "path": "Saturday/thit_trung_mam_tep.jpg",
                "price": "35",
                "name": "Thịt trưng mắm tép",
                "code": "4"
            }
        ]
    },
    {
        "day": "Default",
        "Menu": [
            {
                "path": "ca_kho_mang.jpg",
                "price": "40",
                "name": "Cá kho măng",
                "code": "1"
            },
            {
                "path": "ga_ap_chao.jpg",
                "price": "35",
                "name": "Gà áp chảo",
                "code": "2"
            },
            {
                "path": "suon_rim_dua.jpg",
                "price": "35",
                "name": "Sườn rim dứa",
                "code": "3"
            },
            {
                "path": "thit_trung_mam_tep.jpg",
                "price": "35",
                "name": "Thịt trưng mắm tép",
                "code": "4"
            }
        ]
    },
]


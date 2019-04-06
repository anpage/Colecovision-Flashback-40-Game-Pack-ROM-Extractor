#!/usr/bin/env python3

import os
import zlib

# Rips ROMs and BIOS from the Steam release of Colecovision Flashback

# From v121514
ROMS = [
    {'name': "Antarctic Adventure (USA, Europe).col", 'offset': 0x54d40, 'size': 0x4000, 'crc32': 0x275c800e, },
    {'name': "Aquattack (USA).col", 'offset': 0x58d40, 'size': 0x4000, 'crc32': 0x275a7013, },
    {'name': "Brain Strainers (USA, Europe).col", 'offset': 0x5cd40, 'size': 0x4000, 'crc32': 0x829c967d, },
    {'name': "Bump 'N' Jump (USA, Europe).col", 'offset': 0x60d40, 'size': 0x6000, 'crc32': 0x2b22d4, },
    {'name': "Choplifter! (USA).col", 'offset': 0x66d40, 'size': 0x4000, 'crc32': 0x30e0d48, },
    {'name': "Cosmic Avenger (USA, Europe).col", 'offset': 0x6ad40, 'size': 0x4000, 'crc32': 0x39d4215b, },
    {'name': "Evolution (Canada) [b].col", 'offset': 0x6ed40, 'size': 0x4000, 'crc32': 0xdff01cf7, },
    {'name': "Fathom (USA) [b].col", 'offset': 0x72d40, 'size': 0x4000, 'crc32': 0x9eb58823, },
    {'name': "Flipper Slipper (USA) (Unl) [b].col", 'offset': 0x76d40, 'size': 0x4000, 'crc32': 0x7e97a22e, },
    {'name': "Fortune Builder (USA).col", 'offset': 0x7ad40, 'size': 0x8000, 'crc32': 0x65bbbcb4, },
    {'name': "Frantic Freddy (USA).col", 'offset': 0x82d40, 'size': 0x4000, 'crc32': 0x8615c6e8, },
    {'name': "Frenzy (USA, Europe) [b].col", 'offset': 0x86d40, 'size': 0x6000, 'crc32': 0xbf1ccf04, },
    {'name': "Gateway to Apshai (USA, Europe) [b].col", 'offset': 0x8cd40, 'size': 0x4000, 'crc32': 0x726b64d, },
    {'name': "Gust Buster (USA) [b].col", 'offset': 0x90d40, 'size': 0x4000, 'crc32': 0xf2cac67c, },
    {'name': "Jumpman Junior (USA, Europe) [b].col", 'offset': 0x94d40, 'size': 0x4000, 'crc32': 0x60c69e8, },
    {'name': "Jungle Hunt (USA) [b].col", 'offset': 0x98d40, 'size': 0x6000, 'crc32': 0xe8858484, },
    {'name': "Miner 2049er Starring Bounty Bob (USA, Europe) [b].col", 'offset': 0x9ed40, 'size': 0x6000, 'crc32': 0xb24f10fd, },
    {'name': "Moonsweeper (USA, Europe).col", 'offset': 0xa4d40, 'size': 0x4000, 'crc32': 0x8a303f5a, },
    {'name': "Mountain King (USA).col", 'offset': 0xa8d40, 'size': 0x4000, 'crc32': 0xc173bbec, },
    {'name': "Ms. Space Fury.col", 'offset': 0xacd40, 'size': 0x7C00, 'crc32': 0x4c282755, },
    {'name': "Nova Blast (USA, Europe) [b].col", 'offset': 0xb4b40, 'size': 0x4000, 'crc32': 0xea06f585, },
    {'name': "Oil's Well (USA).col", 'offset': 0xb8b40, 'size': 0x4000, 'crc32': 0xadd10242, },
    {'name': "Omega Race (USA, Europe) [b].col", 'offset': 0xbcb40, 'size': 0x4000, 'crc32': 0x9921ecb5, },
    {'name': "Pepper II (USA, Europe).col", 'offset': 0xc0b40, 'size': 0x4000, 'crc32': 0x53b85e20, },
    {'name': "Quest for Quintana Roo (USA).col", 'offset': 0xc4b40, 'size': 0x4000, 'crc32': 0xeec81c42, },
    {'name': "Rolloverture (USA) [b].col", 'offset': 0xc8b40, 'size': 0x4000, 'crc32': 0xe4585c0a, },
    {'name': "Sammy Lightfoot (USA) [b].col", 'offset': 0xccb40, 'size': 0x4000, 'crc32': 0xc5f69a1b, },
    {'name': "Sir Lancelot (USA) [b].col", 'offset': 0xd0b40, 'size': 0x4000, 'crc32': 0xdd76775d, },
    {'name': "Slurpy (USA).col", 'offset': 0xd4b40, 'size': 0x6000, 'crc32': 0x27f5c0ad, },
    {'name': "Space Fury (USA, Europe).col", 'offset': 0xdab40, 'size': 0x4000, 'crc32': 0xdf8de30f, },
    {'name': "Space Panic (USA, Europe).col", 'offset': 0xdeb40, 'size': 0x4000, 'crc32': 0x5bdf2997, },
    {'name': "Squish 'Em Sam! (USA).col", 'offset': 0xe2b40, 'size': 0x4000, 'crc32': 0x6c82e0cc, },
    {'name': "Super Cross Force (USA) [b].col", 'offset': 0xe6b40, 'size': 0x4000, 'crc32': 0x8093b672, },
    {'name': "Heist, The (USA) [b].col", 'offset': 0xeab40, 'size': 0x6000, 'crc32': 0x6f2e2d84, },
    {'name': "Threshold (USA).col", 'offset': 0xf0b40, 'size': 0x4000, 'crc32': 0x1593f7df, },
    {'name': "Tournament Tennis (USA).col", 'offset': 0xf4b40, 'size': 0x4000, 'crc32': 0xc1d5a702, },
    {'name': "Venture (USA, Europe).col ", 'offset': 0xf8b40, 'size': 0x4000, 'crc32': 0x8e5a4aa3, },
    {'name': "War Room (USA).col", 'offset': 0xfcb40, 'size': 0x6000, 'crc32': 0x261b7d56, },
    {'name': "Wing War (USA).col", 'offset': 0x102b40, 'size': 0x4000, 'crc32': 0x4eeef44, },
    {'name': "Zaxxon (USA, Europe).col", 'offset': 0x106b40, 'size': 0x4000, 'crc32': 0x8cb0891a, },
    {'name': "COLECO.ROM", 'offset': 0x4772c, 'size': 0x2000, 'crc32': 0x3aa93ef3, },  # BIOS
]

if __name__ == '__main__':
    # File is only ~5MB
    f = open("CV40-121514.exe", "rb")
    exe_file = f.read()
    f.close()

    if not os.path.exists("ROMs"):
        os.makedirs("ROMs")

    for rom in ROMS:
        start = rom['offset']
        end = rom['offset']+rom['size']
        rom_data = exe_file[start:end]
        rom_hash = zlib.crc32(rom_data)
        if rom_hash == rom['crc32']:
            rom_file = open("ROMs/" + rom['name'], "wb")
            rom_file.write(rom_data)
            rom_file.close()
        else:
            print("Checksum for ROM \"" + rom['name'] + "\" doesn't match:")
            print("Expected: " + hex(rom['crc32']) + ", Got: " + hex(rom_hash))


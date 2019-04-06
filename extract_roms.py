#!/usr/bin/env python3

import os
import zlib
import re

# Rips ROMs and BIOS from the Steam release of Colecovision Flashback
# Patches bad ROMs to match clean No-Intro dumps

# From v121514
ROMS = [
    {
        'name': "[BIOS] ColecoVision (USA, Europe).col",
        'offset': 0x4772c,
        'size': 0x2000,
        'crc32': 0x3aa93ef3,
    },
    {
        'name': "Antarctic Adventure (USA, Europe).col",
        'offset': 0x54d40,
        'size': 0x4000,
        'crc32': 0x275c800e,
    },
    {
        'name': "Aquattack (USA) [b].col",
        'offset': 0x58d40,
        'size': 0x4000,
        'crc32': 0x275a7013,
        'patch': [
            [0x1A7B, 0xFF], [0x3FFF, 0x7f],
        ],
    },
    {
        'name': "Brain Strainers (USA).col",
        'offset': 0x5cd40,
        'size': 0x4000,
        'crc32': 0x829c967d,
    },
    {
        'name': "Bump 'N' Jump (USA, Europe).col",
        'offset': 0x60d40,
        'size': 0x5000,
        'crc32': 0x9e1fab59,
    },
    {
        'name': "Choplifter! (USA).col",
        'offset': 0x66d40,
        'size': 0x4000,
        'crc32': 0x30e0d48,
    },
    {
        'name': "Cosmic Avenger (USA, Europe).col",
        'offset': 0x6ad40,
        'size': 0x4000,
        'crc32': 0x39d4215b,
    },
    {
        'name': "Evolution (Canada) [b].col",
        'offset': 0x6ed40,
        'size': 0x4000,
        'crc32': 0xdff01cf7,
        'patch': [
            [0x3FFE, 0xFF],
        ],
    },
    {
        'name': "Fathom (USA) [b].col",
        'offset': 0x72d40,
        'size': 0x4000,
        'crc32': 0x9eb58823,
        'patch': [
            [0x3FFF, 0x00],
        ],
    },
    {
        'name': "Flipper Slipper (USA, Europe) [b].col",
        'offset': 0x76d40,
        'size': 0x4000,
        'crc32': 0x7e97a22e,
        'patch': [
            [0x3FFF, 0x09],
        ],
    },
    {
        'name': "Fortune Builder (USA).col",
        'offset': 0x7ad40,
        'size': 0x8000,
        'crc32': 0x65bbbcb4,
    },
    {
        'name': "Frantic Freddy (USA).col",
        'offset': 0x82d40,
        'size': 0x4000,
        'crc32': 0x8615c6e8,
    },
    {
        'name': "Frenzy (USA, Europe).col",
        'offset': 0x86d40,
        'size': 0x5000,
        'crc32': 0x3cacddfb,
    },
    {
        'name': "Gateway to Apshai (USA, Europe).col",
        'offset': 0x8cd40,
        'size': 0x3000,
        'crc32': 0xfdb75be6,
    },
    {
        'name': "Gust Buster (USA) [b].col",
        'offset': 0x90d40,
        'size': 0x4000,
        'crc32': 0xf2cac67c,
        'patch': [
            [0x1D79, 0xFF], [0x1D7B, 0xFF],
            [0x1D7C, 0xFF], [0x1D7D, 0xFF],
            [0x1FFB, 0xFF], [0x1FFD, 0xFF],
            [0x3FFF, 0x00],
        ],
    },
    {
        'name': "Jumpman Junior (USA, Europe).col",
        'offset': 0x94d40,
        'size': 0x4000,
        'crc32': 0x60c69e8,
    },
    {
        'name': "Jungle Hunt (USA) [b].col",
        'offset': 0x98d40,
        'size': 0x6000,
        'crc32': 0xe8858484,
        'patch': [
            [0x447D, 0xFF],
        ],
    },
    {
        'name': "Miner 2049er Starring Bounty Bob (USA, Europe) (v1.1).col",
        'offset': 0x9ed40,
        'size': 0x6000,
        'crc32': 0xb24f10fd,
    },
    {
        'name': "Moonsweeper (USA, Europe).col",
        'offset': 0xa4d40,
        'size': 0x4000,
        'crc32': 0x8a303f5a,
    },
    {
        'name': "Mountain King (USA).col",
        'offset': 0xa8d40,
        'size': 0x4000,
        'crc32': 0xc173bbec,
    },
    {
        'name': "Ms. Space Fury.col",
        'offset': 0xacd40,
        'size': 0x7E00,
        'crc32': 0xdffd8cb4,
    },
    {
        'name': "Nova Blast (USA, Europe).col",
        'offset': 0xb4b40,
        'size': 0x3000,
        'crc32': 0x4491a35b,
    },
    {
        'name': "Oil's Well (USA).col",
        'offset': 0xb8b40,
        'size': 0x4000,
        'crc32': 0xadd10242,
    },
    {
        'name': "Omega Race (USA, Europe) [b].col",
        'offset': 0xbcb40,
        'size': 0x4000,
        'crc32': 0x9921ecb5,
        'patch': [
            [0x3FFE, 0xFF],
        ],
    },
    {
        'name': "Pepper II (USA, Europe).col",
        'offset': 0xc0b40,
        'size': 0x4000,
        'crc32': 0x53b85e20,
    },
    {
        'name': "Quest for Quintana Roo (USA).col",
        'offset': 0xc4b40,
        'size': 0x4000,
        'crc32': 0xeec81c42,
    },
    {
        'name': "Rolloverture (USA) [b].col",
        'offset': 0xc8b40,
        'size': 0x4000,
        'crc32': 0xe4585c0a,
        'patch': [
            [0x1AFD, 0xFF], [0x217D, 0xFF],
            [0x3FFF, 0x4F],
        ],
    },
    {
        'name': "Sammy Lightfoot (USA) [b].col",
        'offset': 0xccb40,
        'size': 0x4000,
        'crc32': 0xc5f69a1b,
        'patch': [
            [0x3FF1, 0xFF], [0x3FF2, 0xFF],
            [0x3FF3, 0xFF], [0x3FF4, 0xFF],
            [0x3FF5, 0xFF], [0x3FF6, 0xFF],
            [0x3FF7, 0xFF], [0x3FF8, 0xFF],
            [0x3FF9, 0xFF], [0x3FFA, 0xFF],
            [0x3FFB, 0xFF], [0x3FFC, 0xFF],
            [0x3FFD, 0xFF], [0x3FFE, 0xFF],
        ],
    },
    {
        'name': "Sir Lancelot (USA) [b].col",
        'offset': 0xd0b40,
        'size': 0x4000,
        'crc32': 0xdd76775d,
        'patch': [
            [0x19CD, 0xFF], [0x21F9, 0xFF],
            [0x3FFE, 0x41], [0x3FFF, 0x39],
        ],
    },
    {
        'name': "Slurpy (USA) [b].col",
        'offset': 0xd4b40,
        'size': 0x39C0,
        'crc32': 0x62792c90,
        'special': 'SLURPY',
    },
    {
        'name': "Space Fury (USA, Europe).col",
        'offset': 0xdab40,
        'size': 0x4000,
        'crc32': 0xdf8de30f,
    },
    {
        'name': "Space Panic (USA, Europe).col",
        'offset': 0xdeb40,
        'size': 0x4000,
        'crc32': 0x5bdf2997,
    },
    {
        'name': "Squish'em Featuring Sam (USA) [b].col",
        'offset': 0xe2b40,
        'size': 0x4000,
        'crc32': 0x6c82e0cc,
        'patch': [
            [0x3FFE, 0x6E], [0x3FFF, 0x20],
        ],
    },
    {
        'name': "Super Cross Force (USA, Europe).col",
        'offset': 0xe6b40,
        'size': 0x3000,
        'crc32': 0x84350129,
    },
    {
        'name': "Heist, The (USA) [b].col",
        'offset': 0xeab40,
        'size': 0x6000,
        'crc32': 0x6f2e2d84,
        'patch': [
            [0x1066, 0x48], [0x5FFE, 0x70],
            [0x5FFF, 0x66],
        ],
    },
    {
        'name': "Threshold (USA).col",
        'offset': 0xf0b40,
        'size': 0x4000,
        'crc32': 0x1593f7df,
    },
    {
        'name': "Tournament Tennis (USA).col",
        'offset': 0xf4b40,
        'size': 0x4000,
        'crc32': 0xc1d5a702,
    },
    {
        'name': "Venture (USA, Europe).col ",
        'offset': 0xf8b40,
        'size': 0x4000,
        'crc32': 0x8e5a4aa3,
    },
    {
        'name': "War Room (USA).col",
        'offset': 0xfcb40,
        'size': 0x6000,
        'crc32': 0x261b7d56,
    },
    {
        'name': "Wing War (USA) [b].col",
        'offset': 0x102b40,
        'size': 0x4000,
        'crc32': 0x4eeef44,
        'patch': [
            [0x3FFF, 0x00],
        ],
    },
    {
        'name': "Zaxxon (USA, Europe).col",
        'offset': 0x106b40,
        'size': 0x6000,
        'crc32': 0x8cb0891a,
    },
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
        end = start + rom['size']
        rom_data = exe_file[start:end]
        rom_hash = zlib.crc32(rom_data)
        if rom_hash == rom['crc32']:
            rom_file = open("ROMs/" + rom['name'], "wb")
            rom_file.write(rom_data)
            rom_file.close()

            if 'patch' in rom.keys():
                rom_data_patched = bytearray(rom_data)
                for patch in rom['patch']:
                    rom_data_patched[patch[0]] = patch[1]
                rom_file_patched = open(
                    "ROMs/" + re.sub(r' \[b\]', '', rom['name']), "wb")
                rom_file_patched.write(rom_data_patched)
                rom_file_patched.close()

            if 'special' in rom.keys():
                # Slurpy needs some padding to match No-Intro
                rom_data_patched = bytearray(
                    rom_data) + bytearray([0xFF]*0x640)
                rom_file_patched = open(
                    "ROMs/" + re.sub(r' \[b\]', '', rom['name']), "wb")
                rom_file_patched.write(rom_data_patched)
                rom_file_patched.close()
        else:
            print("Checksum for ROM \"" + rom['name'] + "\" doesn't match:")
            print("Expected: " + hex(rom['crc32']) + ", Got: " + hex(rom_hash))

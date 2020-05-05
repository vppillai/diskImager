#script to convert a bin file to C array. Specifically written to convert disk image to C file.

from string import Template
import binascii

def make_sublist_group(lst: list, grp: int) -> list:
    """
    Group list elements into sublists.
    make_sublist_group([1, 2, 3, 4, 5, 6, 7], 3) = [[1, 2, 3], [4, 5, 6], 7]
    """
    return [lst[i:i+grp] for i in range(0, len(lst), grp)]

def do_convension(content: bytes) -> str:
    hexstr = binascii.hexlify(content).decode("UTF-8")
    hexstr = hexstr.upper()
    array = ["0x" + hexstr[i:i + 2] + "" for i in range(0, len(hexstr), 2)]
    array = make_sublist_group(array, 10)
    
    return sum(len(a) for a in array ), "\n".join([", ".join(e) + ", " for e in array])



diskImage_c_template=Template("""
/*******************************************************************************
  Flash Memory Disk Image

  Company:
    Microchip Technology Inc.

  File Name:
    diskImage.c

  Summary:
    Flash Memory Disk Image

  Description:
    This file contains FAT12 disk image containing one file.
*******************************************************************************/

// DOM-IGNORE-BEGIN
/*******************************************************************************
* Copyright (C) 2018 Microchip Technology Inc. and its subsidiaries.
*
* Subject to your compliance with these terms, you may use Microchip software
* and any derivatives exclusively with Microchip products. It is your
* responsibility to comply with third party license terms applicable to your
* use of third party software (including open source software) that may
* accompany Microchip software.
*
* THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
* EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
* WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
* PARTICULAR PURPOSE.
*
* IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
* INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
* WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
* BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
* FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
* ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
* THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *******************************************************************************/
// DOM-IGNORE-END

/******************************************************************************
 * This array contains one FAT12 partition disk image with one file FILE.TXT
 * The total size of this disk (array size) is 32768 bytes
 * The area available for actual storage is 30 KB
 ******************************************************************************/

#include "configuration.h"
#include "definitions.h"
#include "usb/src/usb_device_msd_local.h"

const unsigned char 
    __attribute__((keep)) __attribute__((address(DRV_MEMORY_DEVICE_START_ADDRESS)))
    diskImage[$length] = 
{
$diskImage
};
""")

with open('CURIOSITY', 'rb') as file:
    diskImage=file.read()

diskLength , diskArray=do_convension(diskImage)

with open('diskImage.c', 'w') as file: 
    file.write(diskImage_c_template.substitute(length=diskLength,diskImage=diskArray))
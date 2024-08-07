from django.test import TestCase
import datetime

# Create your tests here.

data = ["CONFINED SPACE WORK PERMIT", "EXCAVATION PERMIT", "L.O.T.O", "M.S & R.A", "LIFTING PERMIT MANUAL HANDLING",
        "ROUTES CLEAR OF OBSTRUCTIONS", "HOUSEKEEPING STANDARD ADEQUATE", "MATERIALS STORED SAFELY",
        "CORRECT SIGNAGE POSTED", "BARRIER WORKPLACE", "DUST PROTECTION", "WASTE MATERIALS SEGREGATED",
        "MOBILE PHONE USED OK", "SMOKING ONLY IN DESIGNATED AREAS", "PEOPLE TRAINED FOR SITE",
        "FIRE EXTINGUISHER & WATER BUCKET", "FIRE WATCHER", "FLAMMABLE MATERIALS REMOVED",
        "GAS BOTTLES: STORAGE AND USAGE", "FLAME ARRESTORS ON CYLINDERS & TORCH", "WELDING SCREENS",
        "SCAFFOLDING ERECTED AND USED ACCORDING THE MANUAL", "LADDERS or STEPLADDERS SECURED AND FREE OF DEFECTS",
        "PERSONNEL TRAINED FOR WAH", "FALL ARREST EQUIPMENT WORN AND USED CORRECTLY", "SAFE BODY POSITION",
        "SUPERVISOR FOR WAH ACTIVITIES", "AUTHORIZED PERSONNEL", "LIFTING COORDINATOR or SUPERVISOR",
        "NO PEOPLE UNDER SUSPENDED LOAD", "LIFTING GEARS IN GOOD CONDITION", "TAG LINES", "SHORED EDGES",
        "WALKWAYS AND BRIDGES OVER EXCAVATIONS HAVE GUARDRAILS AND TOE BOARDS", "SAFE AND ENOUGH ACCESS",
        "LADDERS ARE SECURED AND EXTENDED 1 METER ABOVE THE EDGE OF THE TRENCH",
        "SPOILS, MATERIALS & EQUIPMENT SET BACK MINIMUM 1.5 METERS FROM THE EDGE OF THE EXCAVATION",
        "AUTHORIZED ELECTRICIAN", "RESTRICTED ACCESS FOR UNAUTHORIZED PEOPLE", "PROPER INSULATED TOOLS ARE USED",
        "CABINETS ARE CLOSED AND LOCKED", "SPECIFIC PPE IS USED", "PERMIT TO WORK POSTED ON THE ENTRANCE",
        "ALL PERMIT TO WORK REQUIREMENTS ARE IN PLACE", "ONLY AUTHORIZED PERSONNEL FOR CONFINED SPACE ENTRY",
        "WATCHMAN ON MANHOLE", "ALL REGISTERS ARE UPDATED", "CORRECT TOOLS, EQUIPMENT FOR TASK",
        "TOOLS / EQUIPMENT USED CORRECTLY", "TOOLS / EQUIPMENT IN GOOD CONDITION", "OPERATOR CERTIFIED FOR EQUIPMENT",
        "SAFE GUARDS IN PLACE", "CABLES / LEADS", "SITE MACHINERY", "REVERSE ALARM", "BANKSMAN"]

data_after = ['confined space work permit', 'excavation permit', 'l.o.t.o', 'm.s & r.a',
              'lifting permit manual handling', 'routes clear of obstructions', 'housekeeping standard adequate',
              'materials stored safely', 'correct signage posted', 'barrier workplace', 'dust protection',
              'waste materials segregated', 'mobile phone used ok', 'smoking only in designated areas',
              'people trained for site', 'fire extinguisher & water bucket', 'fire watcher',
              'flammable materials removed', 'gas bottles: storage and usage', 'flame arrestors on cylinders & torch',
              'welding screens', 'scaffolding erected and used according the manual',
              'ladders or stepladders secured and free of defects', 'personnel trained for wah',
              'fall arrest equipment worn and used correctly', 'safe body position', 'supervisor for wah activities',
              'authorized personnel', 'lifting coordinator or supervisor', 'no people under suspended load',
              'lifting gears in good condition', 'tag lines', 'shored edges',
              'walkways and bridges over excavations have guardrails and toe boards', 'safe and enough access',
              'ladders are secured and extended 1 meter above the edge of the trench',
              'spoils, materials & equipment set back minimum 1.5 meters from the edge of the excavation',
              'authorized electrician', 'restricted access for unauthorized people', 'proper insulated tools are used',
              'cabinets are closed and locked', 'specific ppe is used', 'permit to work posted on the entrance',
              'all permit to work requirements are in place', 'only authorized personnel for confined space entry',
              'watchman on manhole', 'all registers are updated', 'correct tools, equipment for task',
              'tools / equipment used correctly', 'tools / equipment in good condition',
              'operator certified for equipment', 'safe guards in place', 'cables / leads', 'site machinery',
              'reverse alarm', 'banksman']

data_after2 = []
for n in data_after:
    data_after2.append(n.replace(" ", "_"))

print(data_after2)

from argparse import ArgumentParser
from os.path import join
from os import walk
# Parsing parameters
editing = "atom_edit"
parser = ArgumentParser(description="Searches through CTF writeups for duplicate links on challenge READMEs", epilog="A tool for the CTFs writeups repositories https://github.com/ctfs", )
parser.add_argument("writeupsdir", type=str, help="Directory containing all ctfdirs, e.g. write-ups-2017/")
parser.add_argument("-a", "--atom", dest=editing, action="store_true")
args = parser.parse_args()
if args.atom_edit:
    from os import system
# Files with duplicates counter
dup_files = 0
# Recursively walks through all files in writeups-dir
for root, directories, files in walk(args.writeupsdir):
    for f in files:
        # If its a readme
        if str(f).lower() == "readme.md":
            with open(join(root, f), "rb") as q:
                # Make a list of lines
                lines = q.readlines()
            links = []
            for line in lines:
                # Collect only the links
                if b"* http" in line:
                    links.append(line.strip())
            # Compare length of original and one with duplicates removed
            if len(links) is not len(list(set(links))):
                print("Duplicate links in file", join(root, f))
                dup_files += 1
                # If user chooses to edit duplicate files, open with Atom
                if args.atom_edit:
                    system("atom " + join(root, f))
print(str(dup_files), "files with duplicates found.", ("\nAll " + str(dup_files) + " duplicate files opened with Atom.") if args.atom_edit else "")

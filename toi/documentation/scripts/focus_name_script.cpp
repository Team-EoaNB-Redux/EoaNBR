/*
    Focus name script by Strat

    How to use it:

    1. Copy/Paste file contents of your focus file into input.txt (in this folder)
    2. call this script by doing ./focus_name_script START_OF_FOCUS in either cmd or powershell (in VSCode). Keep folder paths in mind for the latter.
    3. Copy/paste the output from output.txt into the relevant loc file

    START_OF_FOCUS ought to be the starting part of your focus id names (for example, generic_focus_vic_).
    so for generic_focus_vic_establish_a_modern_navy, it will cut off generic_focus_vic_ and use establish_a_modern_navy
    as part of the name.

    Do note that this capitalizes the first letter of the name, and any letter following either a space or dash (-). Therefore
    this does capitalize "A" and "The" and "For" and so on.
*/


#include<iostream>
#include<fstream>
#include<sstream>
#include<vector>
#include<string>
using namespace std;

void replaceAll(std::string& str, const std::string& from, const std::string& to) {
    if(from.empty())
        return;
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // In case 'to' contains 'from', like replacing 'x' with 'yx'
    }
}
void uppercaseFirstLetter(std::string& str){
    if(str.length() == 0) return;

    str[0] = toupper(str[0]);

    size_t i;
    for(i = 1; i < str.length(); i++) {
        if(str[i-1] == ' ' || str[i-1] == '-') str[i] = toupper(str[i]);
    }
}

int main(int argc, char *argv[]){

    string focus_start = "generic_focus_vic_";
    ofstream of;
    
    if(argc>=2){
        focus_start = argv[1];
    }

    of.open("output.txt"); //Open File
    if(!of.is_open()){
        cerr << "Error while opening output file " << endl;
        return 1;
    }
    
    ifstream iff("input.txt");
    if(!iff.is_open()){
        cerr << "Error while opening output file " << endl;
        return 1;
    }

    string line;
    while(getline(iff, line)){
        size_t id_found = line.find("id = ");
        size_t pos_id_found = line.find("relative_position_id");
        size_t hash_found = line.find("#");

        if(pos_id_found == string::npos && id_found!=string::npos && id_found < hash_found){
            string final = line.substr(id_found, hash_found);
            replaceAll(final, "id = ", "");
            replaceAll(final, " ", "");

            string loc = final;
            replaceAll(loc, focus_start, "");
            replaceAll(loc, "_", " ");
            uppercaseFirstLetter(loc);
            of << final << ": \"" << loc << "\"" << endl;
            of << final << "_desc: \"\"" << endl;
        }
    }

    iff.close();
    of.close();

    return 0;
}
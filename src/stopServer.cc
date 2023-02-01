//Author:Elin 
//Create Time:2023-02-01 19:30:32
//Last Modified By:Elin
//Update Time:2023-02-01 19:30:32
#include <iostream>
#include <bits/stdc++.h>
#include <cstdio>


using namespace std;
int main(void)
{
    cout << "[INFO] Trying stop Triton server,please hold on.." << endl;
    FILE *result;
    result = popen("docker ps -l","r");
    int line = 0;
    while (!feof(result))
    {
        char buffer[1024];
        fgets(buffer,1024,result);
        line += 1;
        if(line == 2){
            char *split_line = strtok(buffer," ");
            while(split_line != NULL){
                if(1){
                    string containerID = split_line;
                    string dockerStopcmd = "docker stop " + containerID;
                    const int status = system(dockerStopcmd.c_str());
                    if(status == 0){
                        cout << "[INFO] Triton Sever stopped." << endl;
                        exit(EXIT_SUCCESS);
                    } else {
                        cout << "[ERROR] Failed to stop Triton Server,may be the container doesn run?" << endl;
                        exit(EXIT_FAILURE);
                    }
                }
            }
        }
    }
}
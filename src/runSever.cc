//Author:Elin 
//Create Time:2023-02-01 16:57:08
//Last Modified By:Elin
//Update Time:2023-02-01 16:57:08
#include <iostream>
#include <time.h>
#include <string.h>
using namespace std;
int main(int argc,char *argv [])
{
    // initalize the gpu status ptr to determine Triton boot on GPU mode or CPU mode
    cout << "[INFO] Initalizing..." << endl;
    char *gpuStatus;
    // checking args from input
    if(argc != 2){
        cout << "[ERROR] Expecting args length 2,but got : " << argc << 
            ",determine shutdown the process." << endl;
        exit(EXIT_FAILURE);
    } else {
        gpuStatus = argv[1];
        if(gpuStatus == "1"){
            cout << "[INFO] Setting Triton boot as GPU mode." << endl;
        } else if(gpuStatus == "0"){
            cout << "[INFO] Setting Triton boot as CPU mode.But we suggest that using GPU mode," << 
                "it can reduce down the infercen cycle duration by using gpu acceleration" << endl;
        }
    }
    cout << "[INFO] Initalize Logging info..." << endl;
    // intialize the current time_t variable
    time_t now = time(NULL);
    // intialize the machine localtime structure ptr
    tm *local = localtime(&now);
    // formating the logpath
    char logPath[100];
    strftime(logPath,100,"%Y-%m-%d-%H:%M:%S",local);
    cout << "[INFO] Scanning model repository..." << endl;
    // checking model repository
    const int modelRepoIfExists = system("ls -l $(pwd)/../model_repository");
    if(modelRepoIfExists == 512){
        cout << "[ERROR] Missing model repository,please make sure that exists like : " <<
            "../model_repository and contains the right format of models info and config files that Triton needed."
            << endl;
        cout << "[ERROR] Determine shutdown the process." << endl;
    } else if(modelRepoIfExists == 0){
        cout << "[INFO] Found model repository,try booting Triton Server..." << endl;
    }
    string dockerBootcmd = "nohup docker run --gpus=";
    dockerBootcmd = dockerBootcmd + gpuStatus + " --rm -p8000:8000 -p8001:8001 -p8002:8002 -v $(pwd)/../model_repository:/models nvcr.io/nvidia/tritonserver:22.12-py3 tritonserver --model-repository=/models >> ../logs/" + logPath + ".log &";
    const int run = system(dockerBootcmd.c_str());
    if(run == 0){
        cout << "[INFO] Triton Sever boot sucessfully!Check full logs at : ../logs/" << logPath << ".log" << endl;
        cout << "Dertermine close process and leave Triton as nohup running." << endl;
        exit(EXIT_SUCCESS);
    } else {
        cout << "[ERROR] Fafiled to boot Triton Sever,process shutdown." << endl;
        exit(EXIT_FAILURE);
    }
    return 0;
}
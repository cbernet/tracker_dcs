#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <netdb.h>
#include <string>
#include <stdbool.h>
#include <arpa/inet.h>
#include <iostream>
#include <sstream>
#include <cstring>

//Needed for LOG
#include "../Utils/CommonVisitors.h"

#ifndef __HMP4040_H
#define __HMP4040_H

class HMP4040
{
  private:
    #define PORT              5025
    #define MAX_CMD_BUF       255
    #define MAX_IP_LENGTH     20
    #define TIME_OUT_LIMIT    10
    #define QUESTION_MARK     '?'
    #define END_OF_STRING     '\n'
    int nSockDesc    = 0;
    int nSize        = 0;
    int nConnid      = 0;
    char szIPaddress[MAX_IP_LENGTH];
    char szCmdBuff[MAX_CMD_BUF]      = {0};                 // SCPI command
    char szRecvBuffer[MAX_CMD_BUF]   = {0};                 // Response from device
    struct sockaddr_in servAddr      = {0};
    struct timeval timeOutVar        = {0};
  	struct hostent *hostData         = NULL;


    std::string ipAddress;
    double Ch1[5];
    double Ch2[5];
    double Ch3[5];
    double Ch4[5];

  public:
    HMP4040(std::string pIpAddress);
    int init();
    int reset();

    int setMaximumVoltage (uint8_t pChannel, double pVoltage);
    int setMaximumCurrent(uint8_t pChannel, double pCurrent);
    int setVoltage (uint8_t pChannel, double pVoltage);

    int setChannelStatus(uint8_t pChannel, bool pStatus);
    int genOut(bool pStatus);

    double getVoltage(uint8_t pChannel);
    double getCurrent(uint8_t pChannel);

    std::string sendRecive(const char pCmd[255]);

};

#endif

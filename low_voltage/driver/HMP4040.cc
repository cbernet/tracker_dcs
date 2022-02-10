#include "HMP4040.h"

HMP4040::HMP4040(std::string pIpAddress)
{
  ipAddress = pIpAddress;
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ")" << RESET;
}

int HMP4040::init()
{
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") " << BOLDRED << "Load SEHsettings" << RESET;
  int cSleep = 300;
  setChannelStatus(1,true);
  std::this_thread::sleep_for (std::chrono::milliseconds (cSleep) );
  setMaximumVoltage(1,10.5);
  std::this_thread::sleep_for (std::chrono::milliseconds (cSleep) );
  setMaximumCurrent(1,1.3);
  std::this_thread::sleep_for (std::chrono::milliseconds (cSleep) );
  setVoltage(1,10);
  std::this_thread::sleep_for (std::chrono::milliseconds (cSleep) );
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") " << BOLDRED << "initialised" << RESET;
  return 0;
}

int HMP4040::reset()
{
  std::stringstream s;           // string strem for command line input
  s << "*RST" << "\n" << "SYST:BEEP" << "\n" << "*IDN?";
  std::string str = s.str();
  const char * cmd = str.c_str();
  sendRecive(cmd);

  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") " << BOLDRED << "reset"<<RESET;
  return 0;
}

int HMP4040::setMaximumVoltage(uint8_t pChannel, double pVoltage)
{
  std::stringstream ss;           // string stream for command line input
  ss << "INST OUT" << +pChannel << "\nVolt:PROT " << pVoltage;
  const char * command = ss.str().c_str();
  sendRecive(command);
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") maximum voltage on channel " << +pChannel << " set to:\t" <<BOLDRED<< pVoltage <<"V"<< RESET;
  return 0;
}

int HMP4040::setMaximumCurrent(uint8_t pChannel, double pCurrent)
{
  std::stringstream ss;           // string stream for command line input
  ss << "INST OUT" << +pChannel << "\nCURR " << pCurrent;
  const char * command = ss.str().c_str();
  sendRecive(command);
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") maximum current on channel " << +pChannel << " set to:\t" <<BOLDRED<< pCurrent <<"A"<< RESET;
  return 0;
}
int HMP4040::setVoltage(uint8_t pChannel, double pVoltage)
{
  std::stringstream ss;           // string stream for command line input
  ss << "INST OUT" << +pChannel << "\nVOLT " << pVoltage;
  const char * command = ss.str().c_str();
  sendRecive(command);
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") voltage on channel " << +pChannel << " set to:\t" <<BOLDRED<< pVoltage <<"V"<< RESET;
  return 0;
}

int HMP4040::setChannelStatus(uint8_t pChannel, bool pStatus)
{
  std::stringstream ss;           // string stream for command line input
  ss << "INST OUT" << +pChannel << "\nOUTP:SEL " << pStatus;
  const char * command = ss.str().c_str();

  sendRecive(command);
  if (pStatus == true)
  {
    LOG (INFO) << RED << "HMP4040(" << ipAddress << ") channel "<< +pChannel<<" output " <<BOLDRED<<"activated" << RESET;
  }
  else
  {
    LOG (INFO) << RED << "HMP4040(" << ipAddress << ") channel "<< +pChannel<<" output"  <<BOLDRED<<"deactivated" << RESET;
  }
  return 0;
}
int HMP4040::genOut(bool pStatus)
{
  std::stringstream ss;           // string strem for command line input
  ss << "OUTP:GEN " << pStatus;
  const char * command = ss.str().c_str();

  sendRecive(command);

  if (pStatus)
  {
    LOG (INFO) << RED << "HMP4040(" << ipAddress << ") general output " <<BOLDRED<<"activated" << RESET;
  }
  else
  {
    LOG (INFO) << RED << "HMP4040(" << ipAddress << ") general output " <<BOLDRED<<"deactivated" << RESET;
  }
  return 0;
}

double HMP4040::getVoltage(uint8_t pChannel)
{
  std::stringstream ss;           // string strem for command line input
  ss << "INST OUT" << +pChannel << "\nMEAS:VOLT?";
  const char * command = ss.str().c_str();
  std::string voltageReadout = sendRecive(command);
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") voltage on channel " << +pChannel << ":\t" <<BOLDRED<< voltageReadout <<"V"<< RESET;
  double current = std::stod(voltageReadout);
  return current;
}
double HMP4040::getCurrent(uint8_t pChannel)
{
  std::stringstream ss;           // string strem for command line input
  ss << "INST OUT" << +pChannel << "\nMEAS:CURR?";
  const char * command = ss.str().c_str();
  std::string currentReadout = sendRecive(command);
  LOG (INFO) << RED << "HMP4040(" << ipAddress << ") current on channel " << +pChannel << ":\t" <<BOLDRED<< currentReadout <<"A"<< RESET;
  double current = std::stod(currentReadout);
  return current;
}

std::string HMP4040::sendRecive(const char pCmd[255])
{

//  char szIPaddress[MAX_IP_LENGTH]  = {ipAddress.c_str()};  // IP address
  strncpy(szIPaddress,  ipAddress.c_str(), sizeof( szIPaddress ) );
  for (int i = 0; i < 256; i++)
  {
    szCmdBuff[i] = pCmd[i];
  }

  timeOutVar.tv_sec = TIME_OUT_LIMIT;

	bzero((char*)&servAddr, sizeof(servAddr)); //set the first n=sizeof(...) bytes to zero starting from (char*)&servAddr

  // Filling server address
	inet_pton(AF_INET, szIPaddress, &servAddr.sin_addr); //conversion to 32-bit-internet-address

  // TCP socket creation
  nSockDesc = socket(AF_INET, SOCK_STREAM, 0); //create endpoint for communication

  // Filling server details
  servAddr.sin_family=AF_INET;
  servAddr.sin_port=htons(PORT);

  //connection request to server
  nConnid=connect(nSockDesc, (struct sockaddr*) & servAddr, sizeof(servAddr));

  // Sending command by eliminating new line character
  strcat(szCmdBuff, "\n");
  nSize=send(nSockDesc, szCmdBuff, strlen(szCmdBuff), 0);

  std::string readout = "";

  // Receive only if '?' exists at the end of the SCPI command
  if(szCmdBuff[nSize-2] == QUESTION_MARK)
  {
    // clear the contents of Receive Buffer
    memset(szRecvBuffer, 0, MAX_CMD_BUF);

    // receiving
    nSize=recv(nSockDesc, szRecvBuffer, MAX_CMD_BUF, 0);

    readout = szRecvBuffer;
  }
  close(nSockDesc);
  //get rid of \n at the end of the string
  return readout.substr(0, readout.size()-1);
}

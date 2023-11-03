from sys import path_importer_cache
import numpy as np
from math import copysign

from numpy.core.numeric import outer

from cordic import cordic

class carrier_sync:
    def calcloopgains(self, PhRecBW, dampling_factor, sampl_PS):
        phreclg = PhRecBW * sampl_PS

        theta = phreclg/((dampling_factor + 0.25/dampling_factor)*sampl_PS)
        d = 1 +2*dampling_factor*theta + theta*theta
        
        PhErrGain = 1 #For 8-PSK - look at MATLAB comm.CarrierSynchronizer help page

        PhRecGain = sampl_PS
        #K1
        Kp = (4*dampling_factor*theta/d)/(PhErrGain*PhRecGain)

        #K2
        Ki = (4*theta*theta/d)/(PhErrGain*PhRecGain)

        return Ki, Kp

    def stepImplcordic(self, input ,Ki, Kp):
        inputC = input
        K = (np.sqrt(2) -1)*128
        output = np.zeros(len(inputC)) + 1j*np.zeros(len(inputC))
        phcorr = np.zeros(len(inputC))
        loopFiltState = 0
        IntegFiltState = 0
        DDSPrevInp = 0
        prevSample = 0
        Phase = 0
        Kiacc =0
        Kigen = 0
        iq =0
        qq = 0
        phacc = 0
        errorv = np.zeros(len(inputC))
        lfv = np.zeros(len(inputC))
        for k in range(len(inputC)):
            if np.abs(qq) >= np.abs(iq):
                pherr = copysign(1, qq)*iq - K*copysign(1, iq)*qq/128
            else:
                pherr = K*copysign(1, qq)*iq/128 - copysign(1, iq)*qq

            Kigen = (pherr * Ki) + Kigen
            Kiacc = Kigen
            lfout = (pherr * Kp) + Kigen
            
            phacc = (phacc + lfout)

            qq , iq = cordic( np.real(inputC[k]), np.imag(inputC[k]), phacc, 8)

            output[k] = qq + iq*1j
            phcorr[k] = phacc
            errorv[k] = pherr

        return output, phcorr, errorv

    def stepImpl(input ,Ki, Kp):
        inputC = input
        K = (np.sqrt(2) -1)*32
        output = np.zeros(len(inputC)) + 1j*np.zeros(len(inputC))
        phcorr = np.zeros(len(inputC))
        loopFiltState = 0
        IntegFiltState = 0
        DDSPrevInp = 0
        prevSample = 0
        Phase = 0
        Kiacc =0
        iq =0
        qq = 0
        phacc = 0
        errorv = np.zeros(len(inputC))
        lfv = np.zeros(len(inputC))
        for k in range(len(inputC)):
            if np.abs(qq) >= np.abs(iq):
                pherr = copysign(1, qq)*iq - K*copysign(1, iq)*qq/32
            else:
                pherr = K*copysign(1, qq)*iq/32 - copysign(1, iq)*qq

            qq = np.real(inputC[k])*np.cos(Phase) + np.imag(inputC[k])*np.sin(Phase)
            iq = np.imag(inputC[k])*np.cos(Phase) - np.real(inputC[k])*np.sin(Phase)

            loopFlltOut = pherr * Ki + loopFiltState
            loopFiltState = loopFlltOut

            DDsOUT = DDSPrevInp + IntegFiltState
            IntegFiltState = DDsOUT
            DDSPrevInp = pherr * Kp + loopFlltOut

            Phase = DDsOUT

            output[k] = qq + iq*1j
            phcorr[k] = Phase
            errorv[k] = pherr

        return output, phcorr, errorv
    
def carrsync_cordic_lgc(inp, NbW, damp_fctr, sympsamp):
    cs_inst = carrier_sync()
    Ki, Kp = cs_inst.calcloopgains(NbW, damp_fctr, sympsamp)
    return cs_inst.stepImplcordic(inp, Ki, Kp)
    
#ifndef _CONNCOMP_H
#define _CONNCOMP_H
#include "chirp.hpp"
#include "cblob.h"
#include "blobs.h"

#define RLS_MEMORY          ((uint8_t *)SRAM1_LOC)
#define RLS_MEMORY_SIZE     (SRAM1_SIZE-CL_LUT_SIZE) // bytes

int cc_init(Chirp *chirp);

int32_t cc_setSigRegion(const uint8_t &model, const uint16_t &xoffset, const uint16_t &yoffset, const uint16_t &width, const uint16_t &height);
int32_t cc_setSigPoint(const uint8_t &model, const uint16_t &x, const uint16_t &y);
int32_t cc_setMemory(const uint32_t &location, const uint32_t &len, const uint8_t *data);
int32_t cc_getRLSFrameChirp(Chirp *chirp);
int32_t cc_getRLSFrame(uint32_t *memory, uint8_t *lut, bool sync=true);

#endif

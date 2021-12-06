BLACK=\033[0;30m
RED=\033[0;31m
GREEN=\033[0;32m
ORG=\033[0;33m
BLUE=\033[0;34m
PURPLE=\033[0;35m
CYAN=\033[0;36m
LGREY=\033[0;37m
DGREY=\033[1;30m
LRED=\033[1;31m
LGRN=\033[1;32m
YELLOW=\033[1;33m
LBLUE=\033[1;34m
LPURPLE=\033[1;35m
LCYAN=\033[1;36m
WHITE=\033[1;37m
NC=\033[0m # No Color


CC = g++
CFLAGS+=$(addprefix -I,$(INCLUDE_DIRS))  -Wall -g
CFLAGS+=-MMD -std=c++17
LDFLAGS+=




SOURCE_FILES += $(wildcard $(SRC_DIR)/*.c*)

CFILES   = $(filter %.c,$(SOURCE_FILES))
CPPFILES = $(filter %.cpp,$(SOURCE_FILES))

MKDIR= mkdir -p
DELETE=rm -fr

#-----------------------------------------------------

vpath %.c $(sort $(dir $(CFILES)))
vpath %.cpp $(sort $(dir $(CPPFILES)))

_OBJ = $(notdir $(CFILES:.c=.o))
_OBJ += $(notdir $(CPPFILES:.cpp=.o))

OBJS = $(patsubst %,$(BUILD_DIR)/%,$(_OBJ))

DEPS := $(OBJS:.o=.d)

$(BUILD_DIR)/%.o: %.cpp
	@$(MKDIR) $(BUILD_DIR) || (exit 0)
	@echo Compiling $<
	@$(CC) -c -o $@ $< $(CFLAGS)

$(BUILD_DIR)/%.o: %.c 
	@$(MKDIR) $(BUILD_DIR)  || (exit 0)
	@echo Compiling $<
	$(CC) -c -o $@ $< $(CFLAGS)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $(TARGET) $^ $(CFLAGS) $(LIBS) $(LDIR)

.PHONY: clean

clean:
	@echo cleaning  $(BUILD_DIR)
	@$(DELETE) $(BUILD_DIR)

.PHONY: run

run : $(TARGET)
	$(TARGET)






.PHONY: test
test:
	@echo -e "\n\n"
	@echo -e "$(ORG)--- VARIABLES ---$(NC)"
	@echo -e "TARGET=$(TARGET)"
	@echo -e "BUILD_DIR_HAL=$(BUILD_DIR_HAL)"
	@echo -e "SRC_DIR=$(SRC_DIR)"
	@echo -e ""	
	@echo -e "BASE=$(BASE)"
	@echo -e "CXX=$(CXX)"
	@echo -e "AR=$(AR)"
	@echo -e "CFLAGS=$(CFLAGS)"
	@echo -e "CPPFLAGS=$(CPPFLAGS)"
	@echo -e "CXXFLAGS=$(CXXFLAGS)"
	
	@echo -e "\n\n"
	@echo -e "$(ORG)--- SOURCE FILES ---$(NC)"
	@echo -e $(SOURCE_FILES) | tr '= ' '\n'
	@echo -e ""
	@echo -e "$(ORG)--- OBJS ---$(NC)"
	@echo -e $(OBJS) | tr '= ' '\n'
	@echo -e ""
	@echo -e "$(ORG)--- INCLUDE PATHS ---$(NC)"
	@echo -e $(INC) | tr '= ' '\n'
	@echo -e ""
	

-include $(DEPS)
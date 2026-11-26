BINARY      := vgedit

APP_TITLE	:= vgedit+
APP_AUTHOR 	:= vgmoose
APP_VERSION := 2.2.1

SOURCES		+=	. gui edit
CFLAGS		+= -DUSE_KEYBOARD 
# -D_3DS_MOCK

ifeq (wiiu,$(MAKECMDGOALS))
SOURCES 	+= $(CHESTO_DIR)/libs/wiiu_kbd libs/librpxloader/source
VPATH 		+= $(CHESTO_DIR)/libs/wiiu_kbd
INCLUDES  	+= ../libs/librpxloader/include
endif

# 主仓库统一发起对 libnx/chesto 的临时文本修改（幂等，不提交子模块改动）
ifeq (switch,$(MAKECMDGOALS))
$(shell python3 $(CURDIR)/fix_pie.py)
endif

include libs/chesto/Makefile

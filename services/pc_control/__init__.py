"""
ATLAS Platform & Kontrakt Bot - PC Control & System Management Module
Ushbu modul shaxsiy kompyuterni masofadan boshqarish, monitoring qilish va AI Agent funksiyalarini taqdim etadi.
"""

from .handlers import register_pc_control_handlers, is_pc_control_available

__all__ = ["register_pc_control_handlers", "is_pc_control_available"]

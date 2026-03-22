# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt
import sys
import socket
import subprocess
import json
import threading
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.libraries import pyqt

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class ServiceStatus(Enum):
    """Status of a local service"""

    UNKNOWN = "unknown"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class LocalService:
    """Represents a local web service"""

    name: str
    host: str = "localhost"
    port: int = 8000
    protocol: str = "http"
    path: str = "/"
    description: str = ""
    auto_detect: bool = True
    status: ServiceStatus = ServiceStatus.UNKNOWN
    process_name: str = ""

    @property
    def url(self) -> str:
        """Get the full URL for this service"""
        return f"{self.protocol}://{self.host}:{self.port}{self.path}"

    @property
    def base_url(self) -> str:
        """Get the base URL without path"""
        return f"{self.protocol}://{self.host}:{self.port}"


class ServiceDiscovery(pyqt.QObject):
    """Discovers and monitors local web services"""

    serviceFound = pyqt.Signal(LocalService)
    serviceStatusChanged = pyqt.Signal(str, ServiceStatus)  # service_name, status

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.services: Dict[str, LocalService] = {}
        self.scan_timer = pyqt.QTimer()
        self.scan_timer.timeout.connect(self.scan_services)
        self.common_ports = [3000, 3001, 4000, 5000, 5173, 8000, 8080, 8081, 8888, 9000, 9001]
        self.framework_signatures = {
            "React Dev Server": [3000, 3001],
            "Vue Dev Server": [8080, 8081],
            "Vite Dev Server": [5173],
            "Django Dev Server": [8000],
            "Flask Dev Server": [5000],
            "Express Server": [3000, 8000],
            "Webpack Dev Server": [8080],
            "Next.js Dev Server": [3000],
            "Jupyter Notebook": [8888],
            "Streamlit": [8501],
        }

    def start_discovery(self, interval_ms: int = 5000) -> None:
        """Start automatic service discovery"""
        logma.info("Starting service discovery...")
        self.scan_services()  # Initial scan
        self.scan_timer.start(interval_ms)

    def stop_discovery(self) -> None:
        """Stop automatic service discovery"""
        self.scan_timer.stop()
        logma.info("Service discovery stopped")

    def scan_services(self) -> None:
        """Scan for running local web services"""
        for port in self.common_ports:
            threading.Thread(target=self._check_port, args=(port,), daemon=True).start()

    def _check_port(self, port: int) -> None:
        """Check if a port is open and serving HTTP"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                result = sock.connect_ex(("localhost", port))

                if result == 0:
                    # Port is open, try to determine service type
                    service_name = self._identify_service(port)
                    service = LocalService(name=service_name, host="localhost", port=port, status=ServiceStatus.RUNNING)

                    if service_name not in self.services or self.services[service_name].status != ServiceStatus.RUNNING:
                        self.services[service_name] = service
                        self.serviceFound.emit(service)
                        self.serviceStatusChanged.emit(service_name, ServiceStatus.RUNNING)
                        logma.info(f"Found service: {service_name} on port {port}")
                else:
                    # Check if we previously had a service on this port
                    for name, service in list(self.services.items()):
                        if service.port == port and service.status == ServiceStatus.RUNNING:
                            service.status = ServiceStatus.STOPPED
                            self.serviceStatusChanged.emit(name, ServiceStatus.STOPPED)
                            logma.info(f"Service stopped: {name} on port {port}")

        except Exception as e:
            logma.error(f"Error checking port {port}: {e}")

    def _identify_service(self, port: int) -> str:
        """Try to identify the type of service running on a port"""
        for framework, ports in self.framework_signatures.items():
            if port in ports:
                return f"{framework} (:{port})"
        return f"Local Service (:{port})"

    def add_custom_service(self, service: LocalService) -> None:
        """Manually add a custom service"""
        self.services[service.name] = service
        self.serviceFound.emit(service)
        logma.info(f"Added custom service: {service.name}")

    def remove_service(self, service_name: str) -> None:
        """Remove a service from tracking"""
        if service_name in self.services:
            del self.services[service_name]
            logma.info(f"Removed service: {service_name}")

    def get_service(self, name: str) -> Optional[LocalService]:
        """Get a service by name"""
        return self.services.get(name)

    def get_all_services(self) -> List[LocalService]:
        """Get all discovered services"""
        return list(self.services.values())


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

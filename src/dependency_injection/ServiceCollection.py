from __future__ import annotations
import inspect
from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional, TypedDict, Callable, Dict, Union
from dataclasses import dataclass, field, replace

T = TypeVar("T")

class ServiceLifeTime(Enum):
    InstancePerDependency = auto()
    Scoped = auto()
    Singleton = auto()
    #another possible option for future, named scopes...


class IServiceDecorator(ABC):
    @abstractmethod
    def singleton(self) -> IServiceDecorator:
        pass

    @abstractmethod
    def scoped(self) -> IServiceDecorator:
        pass

    @abstractmethod
    def instancePerDependency(self) -> IServiceDecorator:
        pass

    @abstractmethod
    def As(self, abscraction: Type[T]) -> IServiceDecorator:
        pass

class IScope(ABC):
    @abstractmethod
    def createScope(self) -> ScopeContext:
        pass

    @abstractmethod
    def resolve(self, t: Type[T]) -> T:
        pass

class IServiceCollection(IScope):
    @abstractmethod
    def register(self, t: Type) -> IServiceDecorator:
        pass


class Scope(IScope):
    def __init__(self, services: ServiceCollection):
        self.instances = dict()
        self.services: ServiceCollection = services

    def _get_instance(self, t: Type[T]) -> Optional[T]:
        tName = t.__name__
        if tName in self.instances.keys():
            return self.instances[tName]
        return None

    def _store_instance(self, t: Type[T], instance: T):
        self.instances.update({t.__name__: instance})

    def createScope(self):
        # if I needed scope to be hiearchical, it would be here.
        return ScopeContext(Scope(self.services))

    def resolve(self, t: Type[T]) -> T:
        instance = self._get_instance(t)
        if instance != None:
            return instance
        return self.services.resolve(t, self)


class ScopeContext:
    def __init__(self, scope: Scope):
        self.scope = scope

    def __enter__(self):
        return self.scope

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.scope = None # don't allow this scope to be used again.

@dataclass
class ServiceRegistration:
    name: str
    concrete: Type[T]
    disguised: Type[T]
    life: ServiceLifeTime = field(default=ServiceLifeTime.InstancePerDependency)


class ServiceDescriptor(IServiceDecorator):
    def __init__(self, reg: ServiceRegistration, regDict: Dict[str, ServiceRegistration]):
        self._life = reg.life
        self._concreteName = reg.name
        self._regs = []
        self._services = regDict

    def getConcreteReg(self):
        return self._services.get(self._concreteName)

    def getRegs(self):
        result = []
        if len(self._regs) == 0:
            result.append(self.getConcreteReg())
        else:
            for reg in self._regs:
                result.append(reg)
        return result

    def _removeSelf(self):
        if len(self._regs) == 0:
            del self._services[self._concreteName]

    def _updateLife(self, lifeUpdate: ServiceLifeTime) -> IServiceDecorator:
        for reg in self.getRegs():
            reg = replace(reg, life=lifeUpdate)
            self._services[reg.name] = reg
        return self

    def singleton(self) -> IServiceDecorator:
        return self._updateLife(ServiceLifeTime.Singleton)

    def scoped(self) -> IServiceDecorator:
        return self._updateLife(ServiceLifeTime.Scoped)

    def instancePerDependency(self) -> IServiceDecorator:
        return self._updateLife(ServiceLifeTime.InstancePerDependency)

    def As(self, abstraction: Type[T]) -> IServiceDecorator:
        if len(self._regs) == 0:
            baseReg = self.getConcreteReg()
            self._removeSelf()
        else:
            baseReg = self._regs[0]
        reg = replace(baseReg, disguised=abstraction, name=abstraction.__name__)
        self._regs.append(reg)
        self._services[reg.name] = reg


class ServiceCollection(IServiceCollection):
    def __init__(self, parentCollection: Optional[IServiceCollection] = None):
        self.instances = {}
        self.parentCollection: ServiceCollection = parentCollection
        self.services: Dict[str, ServiceRegistration] = {}
        self.scope = Scope(self)

    def createScope(self) -> ScopeContext:
        return self.scope.createScope()

    def register(self, t: Type[T]) -> IServiceDecorator:
        reg = ServiceRegistration(t.__name__, t, t)
        self.services[reg.name] = reg
        return ServiceDescriptor(reg, self.services)

    def _get_service_reg(self, t: Union[Type[T], str]) -> ServiceRegistration:
        name = t if type(t) == str else t.__name__
        reg = self.services.get(name)
        if reg == None:
            return self.parentCollection._get_service_reg(t)
        return reg

    def _concreteParameters(self, reg: ServiceRegistration) -> [(str, str)]:
        signature = inspect.signature(reg.concrete)
        parameters = signature.parameters
        for param in parameters:
            typeName = parameters[param].annotation
            if hasattr(typeName, '__name__'):
                typeName = typeName.__name__
            yield (param, typeName)


    def _resolve(self, t: Type[T], scope:Scope, stack: [Type[T]] = [], ctorMemo = {}) -> T:
        reg = self._get_service_reg(t)
        if reg == None:
            raise Exception('Service not found: ' + t.__name__)
        name = reg.name
        life = reg.life
        isScope = life == ServiceLifeTime.Scoped
        isTrans = life == ServiceLifeTime.InstancePerDependency
        storeScope = scope if isScope else self.scope

        # quick resolve if already created.
        if not isTrans:
            instance = storeScope._get_instance(t)
            if instance != None:
                return instance

        if t in stack:
            raise Exception('Circular dependency reached: ' + name)
        stack.append(t)

        if name in ctorMemo.keys():
            ctor = ctorMemo[name]
        else:
            arguments = {}
            for (pName, typeName) in self._concreteParameters(reg):
                depType = self._get_service_reg(typeName).concrete
                dep = self._resolve(depType, scope, stack, ctorMemo)
                arguments.update({pName: dep})
            ctor = lambda: reg.concrete(**{**arguments})
            ctorMemo.update({name: ctor})

        instance = ctor()
        if not isTrans:
            storeScope._store_instance(t, instance)
        return instance

    def resolve(self, t: Type[T], scope = None) -> T:
        scope = self.scope if scope == None else scope
        return self._resolve(t, scope, [], {})




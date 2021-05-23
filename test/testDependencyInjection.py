from __future__ import annotations
import unittest
from abc import ABC, abstractmethod
from src.dependency_injection.ServiceCollection import ServiceCollection

class SimpleClass:
    def method(self) -> str:
        return 'SimpleClass'

class DeadSimpleClass:
    Dead = 'simple'

class DependsOnSimpleClass:
    def __init__(self, dep: SimpleClass):
        self.dep = dep

    def method(self) -> str:
        return self.dep.method() + ' also this'

class DepOnDead:
    def __init__(self, dep: DeadSimpleClass):
        self.dep = dep

class DepOnBothSimple:
    def __init__(self, dep: DeadSimpleClass, simple: SimpleClass):
        self.dep = dep
        self.simple = simple

class DependsOnSelf:
    def __init__(self, depSelf: DependsOnSelf):
        self.dep = depSelf

class abstractClass(ABC):

    @abstractmethod
    def method(self):
        pass

class concreteClass(abstractClass):
    def method(self):
        return 'concrete'

class TestDependencyInjection(unittest.TestCase):
    def test_ResisterService(self):
        # Given
        services = ServiceCollection()
        services.register(SimpleClass)

        # When
        simple = services.resolve(SimpleClass)

        # Then
        self.assertEqual(simple.method(), 'SimpleClass')

    def test_GetsDependentService(self):
        # Given
        services = ServiceCollection()
        services.register(SimpleClass)
        services.register(DependsOnSimpleClass)

        # When
        dependsOn = services.resolve(DependsOnSimpleClass)

        # Then
        self.assertEqual(dependsOn.method(), 'SimpleClass also this')

    def test_CanResolve_DepOnDead(self):
        # Given
        services = ServiceCollection()
        services.register(DeadSimpleClass)
        services.register(DepOnDead)

        # When
        a = services.resolve(DepOnDead)

        # Then
        self.assertEqual(a.dep.Dead, 'simple')

    def test_CanResolve_DepOnBoth(self):
        # Given
        services = ServiceCollection()
        services.register(DeadSimpleClass)
        services.register(SimpleClass)
        services.register(DepOnBothSimple)

        # When
        a = services.resolve(DepOnBothSimple)

        # Then
        self.assertEqual(a.dep.Dead, 'simple')
        self.assertEqual(a.simple.method(), 'SimpleClass')

    def test_SelfReference_Throws(self):
        # Given
        services = ServiceCollection()
        services.register(DependsOnSelf)

        # When
        with self.assertRaises(Exception):
            # Then
            services.resolve(DependsOnSelf)

    def test_singleton_resolves_same_instance(self):
        # Given
        services = ServiceCollection()
        services.register(SimpleClass).singleton()

        # When
        a = services.resolve(SimpleClass)
        b = services.resolve(SimpleClass)

        # Then
        self.assertEqual(a, b)

    def test_scope_insideScope_sameInstance(self):
        # Given
        a = None
        b = None
        services = ServiceCollection()
        services.register(SimpleClass).scoped()

        # When
        with services.createScope():
            a = services.resolve(SimpleClass)
            b = services.resolve(SimpleClass)

        # Then
        self.assertEqual(a, b)

    def test_scope_outsideScope_not_sameInstance(self):
        # Given
        a = None
        b = None
        services = ServiceCollection()
        services.register(SimpleClass).scoped()

        # When
        with services.createScope() as scope:
            a = scope.resolve(SimpleClass)
        with services.createScope() as scope:
            b = scope.resolve(SimpleClass)

        # Then
        self.assertNotEqual(a, b)

    def test_scope_nested_callsTo_service(self):
        # Given
        a = b = c = None
        services = ServiceCollection()
        services.register(SimpleClass).scoped()

        # When
        with services.createScope() as scopeOne:
            a = scopeOne.resolve(SimpleClass)
            with services.createScope() as scopeTwo:
                b = scopeTwo.resolve(SimpleClass)
            c = scopeOne.resolve(SimpleClass)

        # Then
        self.assertNotEqual(a, b)
        self.assertEqual(a, c)

    def test_scope_nested_callsTo_scope(self):
        # Given
        a = b = c = None
        services = ServiceCollection()
        services.register(SimpleClass).scoped()

        # When
        with services.createScope() as scopeOne:
            a = scopeOne.resolve(SimpleClass)
            with scopeOne.createScope() as scopeTwo:
                b = scopeTwo.resolve(SimpleClass)
            c = scopeOne.resolve(SimpleClass)

        # Then
        self.assertNotEqual(a, b)
        self.assertEqual(a, c)

    def test_transient_resolves_different_instances(self):
        # Given
        services = ServiceCollection()
        services.register(SimpleClass)

        # When
        a = services.resolve(SimpleClass)
        b = services.resolve(SimpleClass)

        # Then
        self.assertNotEqual(a, b)

    def test_abstractClass_resolvesConcrete(self):
        # Given
        services = ServiceCollection()
        services.register(concreteClass).As(abstractClass)

        # When
        a = services.resolve(abstractClass)

        # Then
        self.assertEqual(a.method(), 'concrete')

if __name__ == '__main__':
    unittest.main()

<!-- Gracias por contribuir. Mantén el principio de sellado (ver SECURITY.md / CONTRIBUTING.md). -->

## Qué cambia
<!-- Una o dos frases. -->

## Tipo
- [ ] Nuevo target vulnerable (self-hosted)
- [ ] Nueva detección de contención (observer)
- [ ] Nuevo adaptador de motor
- [ ] Nueva métrica de análisis
- [ ] Bug fix
- [ ] Docs

## Checklist de ámbito y calidad
- [ ] No añade capacidad de targeting real, evasión ni auto-propagación (SECURITY.md)
- [ ] Si toca `tools.py`: el anclaje al target y el gating de la shell siguen en pie
- [ ] `pytest -q` pasa (o `make smoke`)
- [ ] Si aporta un target: es self-hosted y deliberadamente vulnerable

## Notas / hallazgos
<!-- ¿Descubriste algo al construir esto? Cuéntalo — o abre un Discussion en Show and tell. -->

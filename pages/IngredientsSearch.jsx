import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Box,
  Button,
  Flex,
  Heading,
  HStack,
  Input,
  Tag,
  TagCloseButton,
  Text,
  VStack,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  Image,
  Select,
  useDisclosure,
  useToast,
} from "@chakra-ui/react";
import axios from "axios";
import { useSelector } from "react-redux";
import FeedCard from "../components/Feed/FeedCard";
import { Carousel } from "../components/Feed/SingleRecipeCarousel";
import { buildImageUrl } from "../utils/media";
import { Reveal } from "../components/common/Reveal";
const API = process.env.REACT_APP_API_URL || "http://localhost:5000";

const defaultFlavors = [
  "Afrutado",
  "Especiado",
  "Herbal",
  "Cremoso",
  "Ahumado",
  "Seco",
  "Dulce",
  "Ácido",
  "Amargo",
];

const IngredientsSearch = () => {
  const token = useSelector((s) => s.authReducer.token) || localStorage.getItem("token");
  const toast = useToast();
  const [query, setQuery] = useState("");
  const [ingredients, setIngredients] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [recipes, setRecipes] = useState([]);
  const [selectedList, setSelectedList] = useState([]);
  const [selectedFlavors, setSelectedFlavors] = useState([]);

  const { isOpen, onOpen, onClose } = useDisclosure();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [minutes, setMinutes] = useState(2);
  const [remaining, setRemaining] = useState(2 * 60);
  const [paused, setPaused] = useState(false);
  const timerRef = useRef(null);

  // Buscar sugerencias en la lista maestra de ingredientes
  useEffect(() => {
    const q = query.trim();
    const handler = setTimeout(async () => {
      try {
        const headers = token ? { Authorization: `Bearer ${token}` } : undefined;
        const res = await axios.get(`${API}/ingredients`, { params: { search: q }, headers });
        setSuggestions(res.data?.ingredients || []);
      } catch (err) {
        // No bloquear por error
      }
    }, 300);
    return () => clearTimeout(handler);
  }, [query, token]);

  // Cargar recetas base (para filtrar por ingredientes + sabores)
  const fetchAllRecipes = async () => {
    setLoading(true);
    try {
      const headers = token ? { Authorization: `Bearer ${token}` } : undefined;
      const res = await axios.get(`${API}/recipe/getAllRecipe`, { headers });
      setRecipes(res.data || []);
    } catch (err) {
      toast({ title: "No se pudieron cargar recetas", status: "error" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllRecipes();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const filteredRecipes = useMemo(() => {
    const ing = ingredients.map((i) => i.toLowerCase());
    const fl = selectedFlavors.map((f) => f.toLowerCase());
    let data = recipes;
    if (ing.length > 0) {
      data = data.filter((r) => {
        const rIng = (r.ingredients || []).map((x) => (x || "").toLowerCase());
        return ing.every((q) => rIng.some((ri) => ri.includes(q)));
      });
    }
    if (fl.length > 0) {
      data = data.filter((r) => {
        const rFl = (r.flavors || []).map((x) => (x || "").toLowerCase());
        return fl.some((q) => rFl.includes(q));
      });
    }
    // Orden aproximado por preferencias (flavors): recetas que coincidan con más sabores al inicio
    const weights = new Map();
    fl.forEach((f) => weights.set(f, 1));
    data = [...data].sort((a, b) => {
      const aw = (a.flavors || []).reduce((sum, f) => sum + (weights.get((f || "").toLowerCase()) || 0), 0);
      const bw = (b.flavors || []).reduce((sum, f) => sum + (weights.get((f || "").toLowerCase()) || 0), 0);
      return bw - aw;
    });
    return data;
  }, [recipes, ingredients, selectedFlavors]);

  const addIngredient = () => {
    const raw = (query || "").trim();
    if (!raw) return;
    const parts = raw.split(",").map((p) => p.trim()).filter((p) => p.length > 0);
    setIngredients((prev) => [...prev, ...parts]);
    setQuery("");
  };
  const removeIngredient = (name) => {
    setIngredients((prev) => prev.filter((x) => x !== name));
  };

  const addFlavor = (f) => {
    if (!selectedFlavors.includes(f)) setSelectedFlavors((prev) => [...prev, f]);
  };
  const removeFlavor = (f) => {
    setSelectedFlavors((prev) => prev.filter((x) => x !== f));
  };

  const addToList = (recipe) => {
    if (!selectedList.find((r) => r._id === recipe._id)) setSelectedList((prev) => [...prev, recipe]);
  };
  const removeFromList = (id) => {
    setSelectedList((prev) => prev.filter((r) => r._id !== id));
  };

  const startGuided = () => {
    if (selectedList.length === 0) return toast({ title: "Añade recetas a la lista", status: "info" });
    setCurrentIndex(0);
    setMinutes(2);
    setRemaining(120);
    setPaused(false);
    onOpen();
  };

  useEffect(() => {
    if (!isOpen) return;
    if (paused) return;
    if (remaining <= 0) return;
    timerRef.current = setInterval(() => setRemaining((r) => r - 1), 1000);
    return () => clearInterval(timerRef.current);
  }, [isOpen, paused, remaining]);

  const currentRecipe = selectedList[currentIndex];

  return (
    <Box>
      <Reveal>
      <Box h="40vh" position="relative">
        <Image src="/images/loginImage.jpg" alt="Ingredientes" w="100%" h="100%" objectFit="cover" />
        <VStack position="absolute" inset={0} align="center" justify="center" px={6}>
          <Heading color="white" textShadow="2px 2px 4px #000">Busca cócteles por ingredientes</Heading>
          <Text color="white">Especifica ingredientes y sabores para encontrar mezclas ideales.</Text>
        </VStack>
      </Box>
      </Reveal>

      <Box width="min(80rem,100%)" mx="auto" px={4} py={6}>
        <Heading size="md" mb={3}>Ingredientes</Heading>
        <HStack mb={2} spacing={2} flexWrap="wrap">
          {ingredients.map((name) => (
            <Tag key={name} size="md">
              {name}
              <TagCloseButton onClick={() => removeIngredient(name)} />
            </Tag>
          ))}
        </HStack>
        <HStack gap={2} mb={2}>
          <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Escribe ingredientes o separa por comas" />
          <Button onClick={addIngredient} variant="outline">Añadir</Button>
        </HStack>
        <Text color="gray.600" mb={1}>Sugerencias</Text>
        <HStack spacing={2} flexWrap="wrap">
          {suggestions.slice(0, 12).map((sug) => (
            <Tag key={sug} variant="outline" cursor="pointer" onClick={() => setIngredients((prev) => [...prev, sug])}>{sug}</Tag>
          ))}
        </HStack>

        <Heading size="md" mt={6} mb={3}>Sabores (opcional)</Heading>
        <HStack mb={2} spacing={2} flexWrap="wrap">
          {selectedFlavors.map((f) => (
            <Tag key={f} size="md">
              {f}
              <TagCloseButton onClick={() => removeFlavor(f)} />
            </Tag>
          ))}
        </HStack>
        <HStack spacing={2} flexWrap="wrap" mb={4}>
          {defaultFlavors.map((f) => (
            <Tag key={f} variant="outline" cursor="pointer" onClick={() => addFlavor(f)}>{f}</Tag>
          ))}
        </HStack>

        <Flex justify="space-between" align="center" my={4}>
          <Text color="gray.600">Resultados: {filteredRecipes.length}</Text>
          <Button onClick={startGuided} isDisabled={selectedList.length === 0}>Preparación guiada ({selectedList.length})</Button>
        </Flex>

        <Flex gap={6} align="start" wrap="wrap">
          <Box flex="2 1 60%">
            {loading && <Text>Cargando…</Text>}
            {!loading && filteredRecipes.map((r, idx) => (
              <Reveal key={r._id} delay={0.1 + (idx%6)*0.05}>
                <Box mb={6}>
                  <FeedCard recipe={r} />
                  <HStack mt={2}>
                    <Button size="sm" onClick={() => addToList(r)}>Agregar a la lista</Button>
                    {selectedList.find((x) => x._id === r._id) && (
                      <Button size="sm" variant="outline" onClick={() => removeFromList(r._id)}>Quitar</Button>
                    )}
                  </HStack>
                </Box>
              </Reveal>
            ))}
          </Box>
          <Box flex="1 1 35%" position="sticky" top="1rem">
            <Heading size="sm" mb={2}>Lista para preparar</Heading>
            {selectedList.length === 0 && <Text color="gray.600">Añade recetas para la guía</Text>}
            <VStack align="stretch" spacing={3}>
              {selectedList.map((r) => (
                <Flex key={r._id} justify="space-between" align="center" p={2} borderWidth="1px" borderRadius="md">
                  <Text noOfLines={1}>{r.title}</Text>
                  <Button size="xs" variant="outline" onClick={() => removeFromList(r._id)}>Quitar</Button>
                </Flex>
              ))}
            </VStack>
          </Box>
        </Flex>
      </Box>

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Preparación guiada</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {currentRecipe ? (
              <Box>
                <Heading size="md" mb={2}>{currentRecipe.title}</Heading>
                <HStack align="start" spacing={4} mb={4}>
                  <Box flex="1">
                    {(currentRecipe.images && currentRecipe.images.length > 1) ? (
                      <Carousel images={currentRecipe.images} />
                    ) : (
                    <Image src={buildImageUrl(currentRecipe.images?.[0])} alt={currentRecipe.title} borderRadius="md" />
                    )}
                  </Box>
                  <Box flex="1">
                    <Heading size="sm" mb={2}>Ingredientes</Heading>
                    <VStack align="start" spacing={1} mb={3}>
                      {(currentRecipe.ingredients || []).map((ing, idx) => (
                        <Text key={idx}>• {ing}</Text>
                      ))}
                    </VStack>
                    <Heading size="sm" mb={2}>Método</Heading>
                    <Text mb={3}>{currentRecipe?.caption || "Agitado / Mezclado"}</Text>
                    <Heading size="sm" mb={2}>Pasos</Heading>
                    <VStack align="start" spacing={1}>
                      {(currentRecipe.instructions || []).map((st, idx) => (
                        <Text key={idx}>{idx + 1}. {st}</Text>
                      ))}
                    </VStack>
                  </Box>
                </HStack>

                <HStack my={3}>
                  <Select value={minutes} onChange={(e) => {
                    const m = Number(e.target.value) || 2; setMinutes(m); setRemaining(m * 60);
                  }} width="auto">
                    {[2,3,4,5].map((m) => (<option key={m} value={m}>{m} min</option>))}
                  </Select>
                  <Text>Tiempo restante: {`${String(Math.floor(Math.max(remaining,0)/60)).padStart(2,"0")}:${String(Math.max(remaining,0)%60).padStart(2,"0")}`}</Text>
                  <Button size="sm" onClick={() => setPaused((p) => !p)}>{paused ? "Reanudar" : "Pausar"}</Button>
                  <Button size="sm" variant="outline" onClick={() => setRemaining(minutes * 60)}>Reiniciar</Button>
                </HStack>

                <HStack justify="space-between" mt={4}>
                  <Button variant="outline" onClick={() => {
                    if (currentIndex > 0) { setCurrentIndex((i) => i - 1); setRemaining(minutes * 60); setPaused(false); }
                  }}>Anterior</Button>
                  <Button onClick={() => {
                    if (currentIndex < selectedList.length - 1) { setCurrentIndex((i) => i + 1); setRemaining(minutes * 60); setPaused(false); } else { onClose(); }
                  }}>{currentIndex < selectedList.length - 1 ? "Siguiente" : "Finalizar"}</Button>
                </HStack>
              </Box>
            ) : (
              <Text>Sin recetas en la lista.</Text>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default IngredientsSearch;

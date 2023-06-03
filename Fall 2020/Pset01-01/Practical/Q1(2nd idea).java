import java.util.*;

class Main {

    static class Edge {
        String vertex;
        int weight;

        public Edge(String vertex, int weight) {
            this.vertex = vertex;
            this.weight = weight;
        }
    }

    static List<String> findShortestPath(Map<String, Map<String, Integer>> graph, String start, String end) {
        Map<String, Integer> distances = new HashMap<>();
        Map<String, String> previousVertices = new HashMap<>();
        PriorityQueue<Edge> priorityQueue = new PriorityQueue<>(Comparator.comparingInt(e -> e.weight));

        for (String vertex : graph.keySet()) {
            distances.put(vertex, Integer.MAX_VALUE);
            previousVertices.put(vertex, null);
        }

        distances.put(start, 0);
        priorityQueue.offer(new Edge(start, 0));

        while (!priorityQueue.isEmpty()) {
            Edge currentEdge = priorityQueue.poll();
            String currentVertex = currentEdge.vertex;
            int currentDistance = currentEdge.weight;

            if (currentDistance > distances.get(currentVertex)) {
                continue;
            }

            Map<String, Integer> neighbors = graph.get(currentVertex);
            if (neighbors != null) {
                for (Map.Entry<String, Integer> entry : neighbors.entrySet()) {
                    String neighbor = entry.getKey();
                    int weight = entry.getValue();
                    int distance = currentDistance + weight;

                    if (distance < distances.get(neighbor)) {
                        distances.put(neighbor, distance);
                        previousVertices.put(neighbor, currentVertex);
                        priorityQueue.offer(new Edge(neighbor, distance));
                    }
                }
            }
        }

        List<String> shortestPath = new ArrayList<>();
        String currentVertex = end;
        while (currentVertex != null) {
            shortestPath.add(currentVertex);
            currentVertex = previousVertices.get(currentVertex);
        }

        Collections.reverse(shortestPath);
        return shortestPath;
    }

    static void reducePathWeights(Map<String, Map<String, Integer>> graph, List<String> path) {
        for (int i = 0; i < path.size() - 1; i++) {
            String u = path.get(i);
            String v = path.get(i + 1);
            graph.get(u).put(v, 0);
        }
    }

    static Pair<List<String>, List<String>> findPathsWithCommonality(Map<String, Map<String, Integer>> graph, String a, String b, String c, String d) {
        List<List<String>> pathsAB = new ArrayList<>();
        List<List<String>> pathsCD = new ArrayList<>();

        pathsAB.add(findShortestPath(graph, a, b));

        pathsCD.add(findShortestPath(graph, c, d));

        int maxCommonality = 0;
        List<String> selectedAB = null;
        List<String> selectedCD = null;

        for (List<String> pathAB : pathsAB) {
            for (List<String> pathCD : pathsCD) {
                Set<String> commonVertices = new HashSet<>(pathAB);
                commonVertices.retainAll(pathCD);
                int commonality = commonVertices.size();
                if (commonality > maxCommonality) {
                    maxCommonality = commonality;
                    selectedAB = pathAB;
                    selectedCD = pathCD;
                }
            }
        }

        return new Pair<>(selectedAB, selectedCD);
    }

    public static void main(String[] args) {
        Map<String, Map<String, Integer>> graph = new HashMap<>();
        graph.put("a", new HashMap<>());
        graph.put("b", new HashMap<>());
        graph.put("c", new HashMap<>());
        graph.put("d", new HashMap<>());

        graph.get("a").put("b", 3);
        graph.get("a").put("c", 2);
        graph.get("b").put("d", 4);
        graph.get("c").put("d", 1);

        String a = "a";
        String b = "d";
        String c = "a";
        String d = "b";

        Pair<List<String>, List<String>> paths = findPathsWithCommonality(graph, a, b, c, d);
        List<String> pathAB = paths.getKey();
        List<String> pathCD = paths.getValue();

        reducePathWeights(graph, pathAB);

        System.out.println("Modified Graph:");
        System.out.println(graph);

        System.out.println("Path from 'a' to 'b': " + pathAB);
        System.out.println("Path from 'c' to 'd': " + pathCD);
    }
}
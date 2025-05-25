package org.example.blenderapp.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.*;
import java.util.Objects;

@Service
public class BlenderService {

    private final Path uploadDir = Paths.get("uploads");
    private final Path processedDir = Paths.get("processed");

    // Dynamically resolve a script path relative to the current working directory
    private final Path blenderScriptPath = Paths.get("src", "blender", "process_obj.py").toAbsolutePath();

    public String handleObjFile(MultipartFile file) throws IOException, InterruptedException {
        Files.createDirectories(uploadDir);
        Files.createDirectories(processedDir);

        Path inputPath = uploadDir.resolve(Objects.requireNonNull(file.getOriginalFilename()));
        Path outputPath = processedDir.resolve("processed_" + file.getOriginalFilename());

        Files.copy(file.getInputStream(), inputPath, StandardCopyOption.REPLACE_EXISTING);

        // Use an absolute path to the python script
        ProcessBuilder pb = new ProcessBuilder(
                "blender",
                "--background",
                "--python",
                blenderScriptPath.toString(),
                "--",
                inputPath.toString(),
                outputPath.toString()
        );

        pb.inheritIO(); // Show blender output in the console
        Process process = pb.start();
        int exitCode = process.waitFor();

        if (exitCode != 0) {
            throw new RuntimeException("Blender processing failed");
        }

        return outputPath.toString();
    }
}

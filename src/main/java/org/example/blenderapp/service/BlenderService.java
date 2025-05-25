package org.example.blenderapp.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.nio.file.*;

@Service
public class BlenderService {

    private final Path uploadDir = Paths.get("uploads");
    private final Path processedDir = Paths.get("processed");

    public String handleObjFile(MultipartFile file) throws IOException, InterruptedException {
        Files.createDirectories(uploadDir);
        Files.createDirectories(processedDir);

        Path inputPath = uploadDir.resolve(file.getOriginalFilename());
        Path outputPath = processedDir.resolve("processed_" + file.getOriginalFilename());

        Files.copy(file.getInputStream(), inputPath, StandardCopyOption.REPLACE_EXISTING);

        ProcessBuilder pb = new ProcessBuilder(
                "blender", "--background", "--python", "blender/process_obj.py",
                "--", inputPath.toString(), outputPath.toString()
        );

        pb.inheritIO(); // print Blender output to console
        Process process = pb.start();
        int exitCode = process.waitFor();

        if (exitCode != 0) {
            throw new RuntimeException("Blender processing failed");
        }

        return outputPath.toString();
    }
}

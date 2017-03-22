package ar.edu.itba.sia.c12017.g5.gridlock.utilities;

import com.google.gson.Gson;

import ar.edu.itba.sia.c12017.g5.gridlock.models.Board;

import org.pmw.tinylog.Logger;

import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;

public class BoardParser {
  /*
  * The expected format:
  *  {
  *     "size": {
  *         "rows": Integer,
  *         "columns": Integer
  *     },
  *     "exit": {
  *         "position": {
  *             "x": Integer,
  *             "y": Integer
  *         }
  *     },
  *     "chips":[
  *         {
  *             "main": Boolean,
  *             "start_position": {
  *                 "x": Integer,
  *                 "y": Integer
  *             },
  *             "end_position": {
  *                 "x": Integer,
  *                 "y": Integer
  *             }
  *         },
  *         ...
  *     ]
  *  }
  * */

  /**
   * Parses a board from a json definition.
   * @return parsed board.
   */
  public static Board parse(Path path) {
    try (Reader reader = new InputStreamReader(
            new FileInputStream(path.toString()), StandardCharsets.UTF_8)) {
      BoardModel model = new Gson().fromJson(reader, BoardModel.class);
      return model.toBoard();
    } catch (Exception exception) {
      Logger.error(exception);
    }
    throw new IllegalArgumentException("File doesn't exist or json is invalid");
  }
}

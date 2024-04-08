#include <math.h>

int delayVal = 0;
int motor1 = 9;  // NORTH
int motor2 = 7;  // EAST
int motor3 = 6;  // SOUTH
int motor4 = 3;  // WEST

void setup() {
  Serial.begin(9600);       // Baud rate should match the Unity script
  pinMode(motor1, OUTPUT);  // motor 1 - front
  pinMode(motor2, OUTPUT);  // motor 2 - left
  pinMode(motor3, OUTPUT);  // motor 3 - back
  pinMode(motor4, OUTPUT);  // motor 4 - right
}

// Function to compute the dot product of two arrays of floats
float dotProduct(float a[], float b[]) {
  float result = a[0] * b[0] + a[1] * b[1]; 
  return result;
}

bool facing_same_direction(float dir1[], float dir2[], float dir3[]) {
  normalize(dir1, 2);
  normalize(dir2, 2);
  normalize(dir3, 2);
  float dotProd = dotProduct(dir1, dir2);

  // Check if dir3 is equal to dir1 with a tolerance
  bool equal = true;
  for (int i = 0; i < 2; ++i) {
    if (fabs(dir3[i] - dir1[i]) > 0.001) {
      equal = false;
      break;
    }
  }  
  if (abs(dotProd) == 1 && equal) {
    return true;
  }
  return false;
}

// Function to normalize a vector
void normalize(float vector[], int length) {
  // Calculate magnitude
  float magnitude = 0;
  for (int i = 0; i < length; i++) {
    magnitude += vector[i] * vector[i];
  }
  magnitude = sqrt(magnitude);

  for (int i = 0; i < length; i++) {
    vector[i] /= magnitude;
  }
}

void loop() {

  String data = Serial.readStringUntil('\n');

  // Parse the received string data

  // Position
  float rx1_pos = data.substring(0, data.indexOf(",")).toFloat();
  data = data.substring(data.indexOf(',') + 1);

  float ry1_pos = data.substring(0, data.indexOf(",")).toFloat();
  data = data.substring(data.indexOf(',') + 1);

  float rx2_pos = data.substring(0, data.indexOf(",")).toFloat();
  data = data.substring(data.indexOf(',') + 1);

  float ry2_pos = data.substring(0, data.indexOf(",")).toFloat();
  data = data.substring(data.indexOf(',') + 1);

  float rd1 = data.substring(0, data.indexOf(",")).toFloat();
  data = data.substring(data.indexOf(',') + 1);

  float rd2 = data.substring(0, data.indexOf(",")).toFloat();
  data = data.substring(data.indexOf(',') + 1);

  // float rx2_pos = 10.0; // dummy data
  // float ry2_pos = 10.0;

  // Directions as bearings
  //float rdir1 = data.substring(0, data.indexOf(",")).toFloat() * (PI / 180.0);
  float rdir1 = fmod(rd1 + 270.0, 360.0) * (PI / 180.0);
  float rdir2 = fmod(rd2 + 270.0, 360.0) * (PI / 180.0);

  // Serial.println("rdir: "+ String(degrees(rdir1)));
  // Serial.println("rdir2: " + String(degrees(rdir2)));

  // println the received data
  // Serial.println("Received xpos: " + String(rx1_pos, 2));
  // Serial.println("Received ypos: " + String(ry1_pos, 2));

  // CALCULATIONS
  float diff_x = -rx1_pos + rx2_pos;
  float diff_y = -ry1_pos + ry2_pos;

  float p1_facing_dir[2] = {cos(rdir1), sin(rdir1 - PI) };
  float p2_facing_dir[2] = {cos(rdir2), sin(rdir2 - PI) };
  float p1_p2_vect[2] = { diff_x, diff_y };

  float dot = dotProduct(p1_facing_dir, p1_p2_vect);
  float perpdot = p1_facing_dir[1] * p1_p2_vect[0] -p1_facing_dir[0] * p1_p2_vect[1] ;

  // Calculate the magnitude
  float magA = sqrt(p1_facing_dir[0] * p1_facing_dir[0] + p1_facing_dir[1] * p1_facing_dir[1]);
  float magB = sqrt(p1_p2_vect[0] * p1_p2_vect[0] + p1_p2_vect[1] * p1_p2_vect[1]);

  float dot_denom = magA * magB;
  float theta = degrees(acos(dot / dot_denom));

  if((dot > 0 && perpdot < 0) || (dot < 0 && perpdot < 0)){
    theta = 360 - theta;
  }


  //Serial.println("value of theta: " + String(theta));

  // set all pins to LOW
  digitalWrite(motor1, HIGH);
  digitalWrite(motor2, HIGH);
  digitalWrite(motor3, HIGH);
  digitalWrite(motor4, HIGH);

  float range = 45.0;  // Set the desired range (in degrees)

  // MAXDISTANCE: sqrt(20000)
  // check if users are facing each other
  if (theta <= 10.0 || theta >= 350.0) {

    float diff_x2 = -rx2_pos + rx1_pos;
    float diff_y2 = -ry2_pos + ry1_pos;
    float p2_p1_vect[2] = { diff_x2, diff_y2 };
    float dot2 = dotProduct(p2_facing_dir, p2_p1_vect);
    float magA2 = sqrt(p2_facing_dir[0] * p2_facing_dir[0] + p2_facing_dir[1] * p2_facing_dir[1]);

    float dot_denom2 = magA2 * magB;
    float theta2 = degrees(acos(dot2 / dot_denom2));

    if (theta2 >= 350.0 || theta2 <= 10.0) {
      delayVal = map(int(magB), 0, sqrt(20000), 200, 2000);
      // Serial.println("facing eachother");
      // Serial.println(delayVal);
      digitalWrite(motor1, LOW);
      delay(delayVal);
      digitalWrite(motor1, HIGH);
    }

    else {
      setPins(theta);
      delayVal = 0;
    }
  } else {
    setPins(theta);
    delayVal = 0;
  }


  delay(delayVal);
}

void setPins(float theta) {
  if (theta <= 22.5 || theta > 337.5) {
    // Angle is within the range of the north direction
    digitalWrite(motor1, LOW);
    //Serial.println("Motor 1 (N) vibrating");

  }

  else if (22.5 < theta && theta <= 67.5) {
    // Angle is within *range* degrees to the northeast direction
    digitalWrite(motor1, LOW);
    digitalWrite(motor2, LOW);
    //Serial.println("Motor 1 and 2 (NW) vibrating");

  }

  else if (67.5 < theta && theta <= 112.5) {
    // Angle is within *range* degrees to the east direction
    digitalWrite(motor2, LOW);
    //Serial.println("Motor 2 (W) vibrating");

  }

  else if (112.5 < theta && theta <= 157.5) {
    // Angle is within *range* degrees to the southeast direction
    digitalWrite(motor2, LOW);
    digitalWrite(motor3, LOW);
    //Serial.println("Motor 2 and 3 (SW) vibrating");
  }

  else if (157.5 < theta && theta <= 202.5) {
    // Angle is within *range* degrees to the south direction
    digitalWrite(motor3, LOW);
    //Serial.println("Motor 3 (S) vibrating");

  }

  else if (202.5 < theta && theta <= 247.5) {
    // Angle is within *range* degrees to the southwest direction
    digitalWrite(motor3, LOW);
    digitalWrite(motor4, LOW);
    //Serial.println("Motor 3 and 4 (SE) vibrating");

  }

  else if (247.5 < theta && theta <= 292.5) {
    // Angle is within *range* degrees to the west direction
    digitalWrite(motor4, LOW);
    //Serial.println("Motor 4 (E) vibrating");

  }

  else if (292.5 < theta && theta <= 337.5) {
    // Angle is within *range* degrees to the northwest direction
    digitalWrite(motor4, LOW);
    digitalWrite(motor1, LOW);
    //Serial.println("Motor 4 and 1 (NE) vibrating");
  }
}
